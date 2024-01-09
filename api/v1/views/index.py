#!/usr/bin/python3
"""
    Index view for API.
    Holds status and stats functions.
"""
from flask import jsonify
from models import storage
from . import app_views
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.user import User


@app_views.route('/status', methods=['GET'])
def status():
    """Return OK status. Format == JSON."""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """Retrieves the number of each objects by type."""
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
