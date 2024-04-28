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
    if not all_state:
        abort(404, "State not found")
    list_cities = [city.to_dict() for city in all_state.cities]
    return jsonify(list_cities)


@app_views.route("/cities/<string:city_id>", methods=['GET'])
def get_city(city_id):
    """ get a city by id """
    all_city = models.storage.get(City, city_id)
    if all_city:
        return jsonify(all_city.to_dict())
    else:
        abort(404, "City not found")


@app_views.route("/cities/<string:city_id>", methods=['DELETE'])
def delete_city(city_id):
    """ Delete a city by id """
    all_city = models.storage.get(City, city_id)
    if all_city:
        models.storage.delete(all_city)
        models.storage.save()
        return jsonify({}), 200
    else:
        abort(404, "City not found")


@app_views.route('/states/<state_id>/cities/', methods=['POST'])
def create_city(state_id):
    """ Creates a City """
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    all_state = models.storage.get(State, state_id)
    if not all_state:
        abort(404, "State not found")
    if not request.get_json():
        abort(400, "Not a JSON")
    city_json = request.get_json()
    if "name" not in city_json:
        abort(400, "Missing name")
    city_json["state_id"] = state_id

    new_city = City(**city_json)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<string:city_id>", methods=['PUT'])
def update_city(city_id):
    """ Update a city by id """
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    all_city = models.storage.get(City, city_id)
    if all_city:
        if not request.get_json():
            abort(400, "Not a JSON")
        new_city = request.get_json()
        city_json = ["id", "state_id", "created_at", "updated_at"]
        for k, v in new_city.items():
            if k not in city_json:
                setattr(all_city, k, v)
        all_city.save()
        return jsonify(all_city.to_dict()), 200
    else:
        abort(404)
