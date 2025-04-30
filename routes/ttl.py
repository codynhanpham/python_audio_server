from flask import Blueprint, jsonify, g, request

import time, os
if not hasattr(time, 'time_ns'):
    time.time_ns = lambda: int(time.time() * 1e9)

import utils as utils

ttl_blueprint = Blueprint('ttl', __name__)

@ttl_blueprint.route('/send_ttl_pulse', methods=['GET'])
def send_ttl():
    # Send the TTL pulse
    utils.send_ttl_pulse()

    return jsonify({'success': True, 'message': 'TTL pulse sent.'}), 200