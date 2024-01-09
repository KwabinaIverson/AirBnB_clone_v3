#!/usr/bin/python3
"""First endpoint (route) will be to return the status of your API"""

from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)

# Register blueprint
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def teardown_flask(exception):
    """The Flask app context and event listener. Closes storage."""
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """ Handles 404 erros. """
    msg = 'Not found'
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    app_port = int(os.getenv('HBNB_API_PORT', '5000'))

    # Enable debug mode
    app.debug = True

    app.run(host=app_host, port=app_port, threaded=True)
