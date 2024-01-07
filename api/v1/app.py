#!/usr/bin/python3
"""Module for setting up the API application."""
from flask import Flask
import os
from models import storage
from api.v1.views import app_views
from flask import jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Close the storage engine session."""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Handler for 404 errors that returns
    JSON-formatted 404 status code response.
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
