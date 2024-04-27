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
    state = models.storage.get(State, state_id)
    if not state:
        return abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<string:city_id>", methods=['GET'])
def get_city(city_id):
    """ get a city by id """
    city = models.storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        return abort(404)


@app_views.route("/cities/<string:city_id>", methods=['DELETE'])
def delete_city(city_id):
    """ Delete a city by id """
    city = models.storage.get(City, city_id)
    if city:
        models.storage.delete(city)
        models.storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/states/<state_id>/cities/', methods=['POST'])
def create_city(state_id):
    """ Creates a City """
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    state = models.storage.get(State, state_id)
    if not state:
        return abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json()
    if "name" not in data:
        return abort(400, "Missing name")
    data["state_id"] = state_id

    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<string:city_id>", methods=['PUT'])
def update_city(city_id):
    """ Update a city by id """
    if request.content_type != "application/json":
        return abort(400, "Not a JSON")
    city = models.storage.get(City, city_id)
    if city:
        if not request.get_json():
            return abort(400, "Not a JSON")

        data = request.get_json()
        ignore_keys = ["id", "state_id", "created_at", "updated_at"]

        for k, v in data.items():
            if k not in ignore_keys:
                setattr(city, k, v)
        city.save()
        return jsonify(city.to_dict()), 200
    else:
        return abort(404)
