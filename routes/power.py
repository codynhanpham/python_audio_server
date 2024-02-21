import os
import sys
from flask import Blueprint, Response, g, jsonify, request
import time
if not hasattr(time, 'time_ns'):
    time.time_ns = lambda: int(time.time() * 1e9)

from threading import Thread
import random
import string

import utils as utils
import simpleaudio

power_blueprint = Blueprint('power', __name__)

@power_blueprint.route('/restart', methods=['GET'])
def restart():
    time_ns = time.time_ns()


    restart = request.args.get('restart') or ""
    if restart.lower() != "true":
        print(f"\n{time_ns}: Received /restart --> Info only.")
        text = """
        If you are trying to restart the server, append ?restart=true to the current URL to confirm.

        
        Use this route to force (attempting to force, at least) the server to restart.
        
            This is useful if you want to stop a long-running audio file or playlist.
            Also, if you have added audio or playlist files to the server folder, you can use this route to restart the server and load these new files.

            NOTE that after restarting, the server will use a new log file, similar to how it would when you first start the server.
        """
        return Response(text, mimetype='text/plain'), 200


    print(f"\n{time_ns}: Received /restart?restart=true --> Restarting the server...")
    _startup_cwd = g._startup_cwd
    def restart_server(_startup_cwd):
        # sleep for a bit to allow the response to be sent back to the client
        time.sleep(0.5)

        args = sys.argv[:]
        print('Re-spawning  %s' % ' '.join(args))
        print("\n\n")

        # handle case where we are running from pyinstaller executable
        # normally, if running directly with python, sys.argv[:] --> ['main.py']. Does not include the python executable so we need to add it
        # if running from pyinstaller executable, sys.argv[:] --> ['main.exe'] (windows) or ['main'] (unix). This by itself is enough (it is the executable) so we don't need to add anything
        # but both case, there is a single element in the list --> compare args[0] to sys.executable
        if args[0] != sys.executable:
            args.insert(0, sys.executable)

        # args.insert(0, sys.executable)
        if sys.platform == 'win32':
            args = ['"%s"' % arg for arg in args]

        os.chdir(_startup_cwd)
        os.execv(sys.executable, args)

    simpleaudio.stop_all()
    utils.PLAYLIST_ABORT = True

    # Run the restart function in a separate thread
    thread = Thread(target=restart_server, args=(_startup_cwd,))
    thread.start()

    # send back a 200 response to confirm the restart has been attempted: "message": "Server should be restarting..."
    return jsonify(message="Server should be restarting. Typically, this should take around 10 seconds, depending on the playlists' content."), 200


@power_blueprint.route('/shutdown', methods=['GET'])
def shutdown():
    time_ns = time.time_ns()

    def clean_up_shutdown_tokens():
        # remove expired tokens
        g.SHUTDOWN_TOKENS = [token for token in g.SHUTDOWN_TOKENS if not (token.value is None)]
        utils.SHUTDOWN_TOKENS = g.SHUTDOWN_TOKENS

    # The request has a valid shutdown token --> shutdown the server
    shutdownToken = request.args.get('token') or ""
    if shutdownToken != "" and any(token.value == shutdownToken for token in g.SHUTDOWN_TOKENS):
        print(f"\n{time_ns}: Received /shutdown?token={shutdownToken} (OK) --> Shutting down the server...")
        # kill the server
        def shutdown():
            # sleep for a bit to allow the response to be sent back to the client
            time.sleep(0.5)

            print("Shutting down the server...")
            os._exit(0)

        # clean up the shutdown tokens
        clean_up_shutdown_tokens()

        simpleaudio.stop_all()
        utils.PLAYLIST_ABORT = True

        # Run the shutdown function in a separate thread
        thread = Thread(target=shutdown)
        thread.start()

        # send back a 200 response to confirm the shutdown has been attempted: "message": "Server should be shutting down..."
        return jsonify(message="The light flashes in the corner of my eye... The server should be shutting down. You will need to access the server (computer) directly to start the audio server back up again."), 200
    elif shutdownToken != "":
        print(f"\n{time_ns}: Received /shutdown?token={shutdownToken} (Invalid) --> Invalid shutdown token.")

        # clean up the shutdown tokens
        clean_up_shutdown_tokens()

        return jsonify(message="Invalid shutdown token."), 400
    

    # Otherwise, the request does not have a valid shutdown token --> send back a 200 response with a shutdown token if the request has the shutdown query parameter, or send back a 200 response with instructions on how to shutdown the server if the request does not have the shutdown query parameter
    shutdown = request.args.get('shutdown') or ""
    if shutdown != "YES_iamsureshutmedown":
        print(f"\n{time_ns}: Received /shutdown --> Info only.")
        text = """
        If you are trying to shutdown the server, append `?shutdown=YES_iamsureshutmedown` to the current URL to get a confirm token.

        You WILL NOT be able to start the server again without manually starting it again, directly by accessing the server computer. If you do not have access to the server computer, YOU WILL NOT BE ABLE TO START THE SERVER AGAIN.

        
        Use this route to force (attempting to force, at least) the server to shutdown.
        
            This is useful if you want to stop a long-running audio file or playlist. If this is your use case, consider using /restart instead.
        """

        # clean up the shutdown tokens
        clean_up_shutdown_tokens()

        return Response(text, mimetype='text/plain'), 200
    

    # send back a 200 response with a shutdown token
    print(f"\n{time_ns}: Received /shutdown?shutdown=YES_iamsureshutmedown --> Sending back a shutdown token.")
    
    # generate a random 12-character string alphanumeric and "-_" characters
    shutdownToken = ''.join(random.choices(string.ascii_letters + string.digits + "-_", k=12))
    expiringVar = utils.ExpiringVariable(shutdownToken, 60) # expire in 60 seconds

    # clean up the shutdown tokens
    clean_up_shutdown_tokens()

    g.SHUTDOWN_TOKENS.append(expiringVar)
    utils.SHUTDOWN_TOKENS = g.SHUTDOWN_TOKENS

    return jsonify(shutdown_token=shutdownToken, route=f"/shutdown?token={shutdownToken}", message="The shutdown token will expire in 60 seconds."), 200