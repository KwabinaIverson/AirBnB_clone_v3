#!/usr/bin/python3
""" The views for the API """

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def get_status():
    """Gets status code of the API."""
    return jsonify(status='OK')
