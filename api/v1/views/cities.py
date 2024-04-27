#!/usr/bin/python3

""" citie """

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.state import State
import models


@app_views.route("/states/<string:state_id>/cities", methods=['GET'])
def get_cities(state_id):
    """ get all cities by state id """
    all_state = models.storage.get(State, state_id)
    if all_state is None:
        abort(404, "State not found")
    list_cities = [city.to_dict() for city in all_state.cities]
    return jsonify(list_cities)


@app_views.route("/cities/<string:city_id>", methods=['GET'])
def get_city(city_id):
    """ get a city by id """
    all_city = models.storage.get(City, city_id)
    if all_city is None:
        abort(404, "City not found")
    return jsonify(all_city.to_dict())


@app_views.route("/cities/<string:city_id>", methods=['DELETE'])
def delete_city(city_id):
    """ Delete a city by id """
    all_city = models.storage.get(City, city_id)
    if all_city is None:
        abort(404, "City not found")
    models.storage.delete(all_city)
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities/', methods=['POST'])
def create_city(state_id):
    """ Creates a City """
    all_state = models.storage.get(State, state_id)
    if not all_state:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")

    city = City(state_id=state_id, **request.get_json())
    city.save()

    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<string:city_id>", methods=['PUT'])
def update_city(city_id):
    """ Update a city by id """
    all_city = models.storage.get(City, city_id)
    if all_city is None:
        abort(404, "City not found")
    city_json = request.get_json()
    if city_json is None:
        abort(400, 'Not a JSON')
    for k, v in city_json.items():
        setattr(all_city, k, v)
    all_city.save()
    return jsonify(all_city.to_dict()), 200
