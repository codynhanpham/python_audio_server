from flask import Blueprint, Response, redirect, send_from_directory
import time
if not hasattr(time, 'time_ns'):
    time.time_ns = lambda: int(time.time() * 1e9)

GUI_blueprint = Blueprint('GUI_page', __name__, static_folder='static')

@GUI_blueprint.route('/')
def app_page():
    # Serve the HTML and related content from the /webpages/app folder
    return send_from_directory('static', 'main_app.html')


# Redirect /gui (or /gui/)to /app
@GUI_blueprint.route('/gui')
@GUI_blueprint.route('/gui/')
@GUI_blueprint.route('/app')
@GUI_blueprint.route('/app/')
def gui_redirect():
    return redirect('/')