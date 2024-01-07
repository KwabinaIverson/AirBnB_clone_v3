#!/usr/bin/python3
""" The views for the API """

from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """Gets status code of the API."""
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """Retrieves the number of each objects by type"""
    objs = {
        'amenities': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review,
        'states': State,
        'users': User
    }

    for key, value in objs.items():
        objs[key] = storage.count(value)
    return jsonify(objs)
