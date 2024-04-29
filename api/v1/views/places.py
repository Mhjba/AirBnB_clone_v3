#!/usr/bin/python3
""" Handles everything related to places """

from models import storage
from models.city import City
from models.state import State
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route("/cities/<string:city_id>/places", methods=['GET'])
def get_places_by_city(city_id):
    """ get all places """
    all_city = models.storage.get(City, city_id)
    if not all_city:
        return abort(404)
    city_obj = []
    for place in all_city.places:
        city_obj.append(place.to_dict())
    return jsonify(city_obj)


@app_views.route("/places/<string:place_id>", methods=['GET'])
def get_place(place_id):
    """ get place """
    gt_place = models.storage.get(Place, place_id)
    if gt_place is None:
        return abort(404)
    return jsonify(gt_place.to_dict())


@app_views.route("/places/<string:place_id>", methods=['DELETE'])
def delete_place_by_id(place_id):
    """
    Delete a place by id
    """
    place_inst = storage.get(Place, place_id)
    if place_inst is None:
        abort(404)
    storage.delete(place_inst)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<string:city_id>/places', methods=['POST'])
def create_new_place(city_id):
    """
    Create a new place
    """
    get_city = storage.get(City, city_id)
    if get_city is None:
        abort(404)
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in req_json:
        abort(400, 'Missing user_id')
    user_data = storage.get("User", req_json['user_id'])
    if user_data is None:
        abort(404)
    if 'name' not in req_json:
        abort(400, 'Missing name')
    req_json['city_id'] = city_id
    place_inst = Place(**req_json)
    place_inst.save()
    return jsonify(place_inst.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def updates_place(place_id):
    """
    Update an place by id
    """
    place_inst = storage.get(Place, place_id)
    if place_inst is None:
        abort(404)
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    for idx, idy in req_json.items():
        if idx not in ['id', 'city_id', 'user_id', 'updated_at',
                       'created_at']:
            setattr(place_inst, idx, idy)
    place_inst.save()
    return jsonify(place_inst.to_dict()), 200
