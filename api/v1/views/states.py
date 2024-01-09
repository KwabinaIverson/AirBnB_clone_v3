#!/usr/bin/python3
"""View for State objects that handles all default RESTFul API actions."""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Retrieves the list of all State objects.

    Returns:
        List of State objects in JSON format.
    """
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a State object.

    Args:
        state_id (str): ID of the State.

    Returns:
        State object in JSON format.

    Raises:
        NotFound: If the state_id is not linked to any State object.
    """
    state = storage.get(State, state_id)
    if not state:
        raise NotFound(description='State not found')
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State object.

    Args:
        state_id (str): ID of the State.

    Returns:
        Empty dictionary with status code 200.

    Raises:
        NotFound: If the state_id is not linked to any State object.
    """
    state = storage.get(State, state_id)
    if not state:
        raise NotFound(description='State not found')
    state.delete()
    storage.save()
    return jsonify({}), 200

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creates a State object.

    Returns:
        New State object in JSON format with status code 201.

    Raises:
        BadRequest: If the HTTP body request is not valid JSON.
        BadRequest: If the dictionary doesn’t contain the key name.
    """
    if not request.is_json:
        raise BadRequest(description='Not a JSON')
    data = request.get_json()
    if 'name' not in data:
        raise BadRequest(description='Missing name')
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object.

    Args:
        state_id (str): ID of the State.

    Returns:
        Updated State object in JSON format with status code 200.

    Raises:
        NotFound: If the state_id is not linked to any State object.
        BadRequest: If the HTTP body request is not valid JSON.
    """
    state = storage.get(State, state_id)
    if not state:
        raise NotFound(description='State not found')
    if not request.is_json:
        raise BadRequest(description='Not a JSON')
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
