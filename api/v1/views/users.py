#!/usr/bin/python3

"""
module: api/v1/views/users
"""

from flask import jsonify, abort, request
from models import storage
from . import app_views
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
       Gets all User objects. Return objects in JSON.
    """
    users = storage.all(User)
    user_js = [user.to_dict() for user in users.values()]
    return jsonify(user_js)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
       Return User obj with id == user_id.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def del_user(user_id):
    """
       Removes User obj from storage.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
        Creates new User obj. Return JSON representation of new obj.
    """
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    if 'email' not in data:
        abort(400, description="Missing email")
    if 'password' not in data:
        abort(400, description="Missing password")
    user = User(**data)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
       Updates User obj wit id == user_id.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
