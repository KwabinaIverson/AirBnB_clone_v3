#!/usr/bin/python3
"""
    First endpoint (route) will be to return the status of your API
"""

from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS

app = Flask(__name__)

app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
app_port = int(os.getenv('HBNB_API_PORT', '5000'))
app.url_map.strict_slashes = False
# Register blueprint
app.register_blueprint(app_views, url_prefix="/api/v1")
# CORS
CORS(app, resources={'/*': {'origins': app_host}})


@app.teardown_appcontext
def teardown_flask(exception):
    """The Flask app context and event listener. Closes storage."""
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """ Handles 404 erros. """
    msg = 'Not found'
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def error_400(error):
    """
    Handles the 400 HTTP error code.

    Args:
        error: The error object associated with the 400 error.

    Returns:
        A JSON response with an error message and a 400 status code.
    """
    msg = 'Bad request'
    if isinstance(error, Exception) and hasattr(error, 'description'):
        msg = error.description
    return jsonify(error=msg), 400

if __name__ == '__main__':
    app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    app_port = int(os.getenv('HBNB_API_PORT', '5000'))

    # Enable debug mode
    app.debug = True

    app.run(host=app_host, port=app_port, threaded=True)
