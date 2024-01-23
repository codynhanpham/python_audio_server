import os
import sys
from flask import Blueprint, Response, g, jsonify, request
import time
if not hasattr(time, 'time_ns'):
    time.time_ns = lambda: int(time.time() * 1e9)

from threading import Thread

power_blueprint = Blueprint('power', __name__)

@power_blueprint.route('/restart', methods=['GET'])
def restart():
    restart = request.args.get('restart') or ""
    if restart.lower() != "true":
        text = """
        If you are trying to restart the server, append ?restart=true to the current URL to confirm.

        
        Use this route to force (attempting to force, at least) the server to restart.
        
            This is useful if you want to stop a long-running audio file or playlist.
            Also, if you have added audio or playlist files to the server folder, you can use this route to restart the server and load these new files.

            NOTE that after restarting, the server will use a new log file, similar to how it would when you first start the server.
        """
        return Response(text, mimetype='text/plain'), 200

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

    # Run the restart function in a separate thread
    thread = Thread(target=restart_server, args=(_startup_cwd,))
    thread.start()

    # send back a 200 response to confirm the restart has been attempted: "message": "Server should be restarting..."
    return jsonify(message="Server should be restarting. Typically, this should take less than 7 seconds."), 200


@power_blueprint.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown = request.args.get('shutdown') or ""
    if shutdown != "iamsureshutmedown_YES":
        text = """
        If you are trying to shutdown the server, append `?shutdown=iamsureshutmedown_YES` to the current URL to confirm.

        You WILL NOT be able to start the server again without manually starting it again, directly by accessing the server computer. If you do not have access to the server computer, YOU WILL NOT BE ABLE TO START THE SERVER AGAIN.

        
        Use this route to force (attempting to force, at least) the server to shutdown.
        
            This is useful if you want to stop a long-running audio file or playlist. If this is your use case, consider using /restart instead.
        """
        return Response(text, mimetype='text/plain'), 200
    

    # kill the server
    def shutdown():
        # sleep for a bit to allow the response to be sent back to the client
        time.sleep(0.5)

        print("Shutting down the server...")
        os._exit(0)

    # Run the shutdown function in a separate thread
    thread = Thread(target=shutdown)
    thread.start()

    # send back a 200 response to confirm the shutdown has been attempted: "message": "Server should be shutting down..."
    return jsonify(message="The light flashes in the corner of my eye... The server should be shutting down. You will need to access the server (computer) directly to start the audio server back up again."), 200