#!/usr/bin/python3
"""View for User object that handles all default RESTFul API actions"""

from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.user import User
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieves the list of all User objects.

    Returns:
        List of User objects in JSON format.
    """
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
    Retrieves a User object.

    Args:
        user_id (str): ID of the User.

    Returns:
        User object in JSON format.

    Raises:
        NotFound: If the user_id is not linked to any User object.
    """
    user = storage.get(User, user_id)
    if not user:
        raise NotFound(description='User not found')
    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a User object.

    Args:
        user_id (str): ID of the User.

    Returns:
        Empty dictionary with status code 200.

    Raises:
        NotFound: If the user_id is not linked to any User object.
    """
    user = storage.get(User, user_id)
    if not user:
        raise NotFound(description='User not found')
    user.delete()
    storage.save()
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Creates a User object.

    Returns:
        New User object in JSON format with status code 201.

    Raises:
        BadRequest: If the HTTP request body is not valid JSON.
        BadRequest: If the dictionary doesn’t contain the key email or password.
    """
    if not request.is_json:
        raise BadRequest(description='Not a JSON')

    data = request.get_json()
    if 'email' not in data:
        raise BadRequest(description='Missing email')
    if 'password' not in data:
        raise BadRequest(description='Missing password')

    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    Updates a User object.

    Args:
        user_id (str): ID of the User.

    Returns:
        Updated User object in JSON format with status code 200.

    Raises:
        NotFound: If the user_id is not linked to any User object.
        BadRequest: If the HTTP request body is not valid JSON.
    """
    user = storage.get(User, user_id)
    if not user:
        raise NotFound(description='User not found')

    if not request.is_json:
        raise BadRequest(description='Not a JSON')

    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)

    user.save()
    return jsonify(user.to_dict()), 200
