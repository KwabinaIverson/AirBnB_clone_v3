#!/usr/bin/python3
""" New view for City objects that handles all default RESTFul API actions. """

from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest
from api.v1.views import app_views
from models import storage
from models.state import State

ALLOWED_METHODS = ['GET', 'POST', 'PUT', 'DELETE']
"""Methods allowed for the states endpoint."""

@app_views.route('/states', methods=ALLOWED_METHODS)
@app_views.route('/states/<state_id>', methods=ALLOWED_METHODS)
def handle_request(state_id=None):
    """ The method handler for the states endpoint. """

    # HTTP methods to corresponding functions
    handlers = {
        'GET': get_states,
        'DELETE': remove_state,
        'PUT': update_state,
        'POST': add_state,
    }
    # if the request method is in the handlers
    if request.method in handlers:
        return handlers[request.method](state_id)
    else:
        raise MethodNotAllowed(valid_methods=list(handlers.keys()))

def get_states(state_id=None):
    """ Get state if there's id or get all states. """
    all_states = storage.all(State).values()
    # Return state if `id` else `NotFound`
    if state_id:
        response = list(filter(lambda x: x.id == state_id, all_states))
        if response:
            return jsonify(response[0].to_dict())
        else:
            raise NotFound()
    # Return all states
    all_states = list(map(lambda x: x.to_dict(), all_states))
    return jsonify(all_states)

def add_states(state_id=None):
    """ Create/add new state. """
    data = request.get_json()
    if type(data) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'name' not in data:
        raise BadRequest(description='Missing name')
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201

def remove_state(state_id=None):
    """ Removes state with id. """
    all_states = storage.all(State).values()
    response = list(filter(lambda x: x.id == state_id, all_states))
    if response:
        storage.delete(response[0])
        storage.save()
        return jsonify({}), 200
    raise NotFound()

def update_state(state_id=None):
    """ Update/change state with a given id. """
    xkeys = ('id', 'created_at', 'updated_at')
    all_states = storage.all(State).values()
    response = res = list(filter(lambda x: x.id == state_id, all_states))
    if response:
        data = request.get_json()
        if type(data) is not dict:
            raise BadRequest(description='Not a JSON')
        old_state = res[0]
        for key, value in data.items():
            if key not in xkeys:
                setattr(old_state, key, value)
        old_state.save()
        return jsonify(old_state.to_dict()), 200
    raise NotFound()
