#!/usr/bin/python3
"""View for City objects that handles all default RESTFul API actions"""

# api/v1/views/cities.py
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):
    """
    Retrieves the list of all City objects of a State.

    Args:
        state_id (str): ID of the State.

    Returns:
        List of City objects in JSON format.

    Raises:
        NotFound: If the state_id is not linked to any State object.
    """
    state = storage.get(State, state_id)
    if not state:
        raise NotFound(description='State not found')

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a City object.

    Args:
        city_id (str): ID of the City.

    Returns:
        City object in JSON format.

    Raises:
        NotFound: If the city_id is not linked to any City object.
    """
    city = storage.get(City, city_id)
    if not city:
        raise NotFound(description='City not found')
    return jsonify(city.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a City object.

    Args:
        city_id (str): ID of the City.

    Returns:
        Empty dictionary with status code 200.

    Raises:
        NotFound: If the city_id is not linked to any City object.
    """
    city = storage.get(City, city_id)
    if not city:
        raise NotFound(description='City not found')
    city.delete()
    storage.save()
    return jsonify({}), 200

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """
    Creates a City object.

    Args:
        state_id (str): ID of the State.

    Returns:
        New City object in JSON format with status code 201.

    Raises:
        NotFound: If the state_id is not linked to any State object.
        BadRequest: If the HTTP body request is not valid JSON.
        BadRequest: If the dictionary doesn’t contain the key name.
    """
    state = storage.get(State, state_id)
    if not state:
        raise NotFound(description='State not found')

    if not request.is_json:
        raise BadRequest(description='Not a JSON')

    data = request.get_json()
    if 'name' not in data:
        raise BadRequest(description='Missing name')

    new_city = City(state_id=state_id, **data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201

@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    Updates a City object.

    Args:
        city_id (str): ID of the City.

    Returns:
        Updated City object in JSON format with status code 200.

    Raises:
        NotFound: If the city_id is not linked to any City object.
        BadRequest: If the HTTP request body is not valid JSON.
    """
    city = storage.get(City, city_id)
    if not city:
        raise NotFound(description='City not found')

    if not request.is_json:
        raise BadRequest(description='Not a JSON')

    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    city.save()
    return jsonify(city.to_dict()), 200
