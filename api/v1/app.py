#!/usr/bin/python3
"""
module: api/v1/app

App logic for API
"""
import os
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, origins="0.0.0.0")


@app.teardown_appcontext
def close_storage(exception):
    """Close storage."""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Return a 404 error code status if resource not found."""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))

    app.run(host=host, port=port, threaded=True, debug=True)
