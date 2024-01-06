#!/usr/bin/python3
"""Index module to set up status route."""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return the status of the API."""
    return jsonify({"status": "OK"})