from flask import Blueprint, Response

ping_blueprint = Blueprint('ping', __name__)

@ping_blueprint.route('/ping', methods=['GET'])
def ping():
    return Response("pong", mimetype='text/plain'), 200