#!/usr/bin/python3
"""Handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.state import State, City
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    else:
        cities = state.cities
        return jsonify([city.to_dict() for city in cities])

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def post_city(state_id):
    data = request.get_json(silent=True)
    if not data:
        abort(400)
    if 'name' not in data:
        abort(400)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    new_city = City(**data)
    new_city.state_id = state_id
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201
