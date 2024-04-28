i#!/usr/bin/python3
""" Handles everything related to places """

from models import storage
from models.city import City
from models.state import State
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route("/cities/<string:city_id>/places", methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """
    Retrieve all places by city id given
    """
    get_city = storage.get(City, city_id)
    if get_city is None:
        abort(404)
    place_inst = get_city.places
    all_places = []
    for item in place_inst:
        all_places.append(item.to_dict())
    return jsonify(all_places)


@app_views.route("/places/<string:place_id>", methods=['GET'],
                 strict_slashes=False)
def get_place_by_id(place_id):
    """
    Reyrieves a place by id
    """
    place_inst = storage.get(Place, place_id)
    if place_inst is None:
        abort(404)
    return jsonify(place_inst.to_dict())

