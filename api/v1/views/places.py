#!/usr/bin/python3
""" Places """

from models import storage
from models.city import City
from models.state import State
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from flask import abort, jsonify, request
import models


@app_views.route('/cities/<city_id>/places/', methods=['GET'])
def list_places_of_city(city_id):
    """ get all places """
    all_city = models.storage.get(City, city_id)
    if not all_city:
        return abort(404)
    city_obj = []
    for place in all_city.places:
        city_obj.append(place.to_dict())
    return jsonify(city_obj)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """ get place """
    gt_place = models.storage.get(Place, place_id)
    if gt_place is None:
        return abort(404)
    return jsonify(gt_place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """ Delete place """
    dl_place = models.storage.get(Place, place_id)
    if dl_place is None:
        return abort(404)
    models.storage.delete(dl_place)
    models.storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """ Create place """
    """ Creates a City """
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    cr_place = models.storage.get(State, city_id)
    if not cr_place:
        abort(404, "State not found")
    if not request.get_json():
        abort(400, "Not a JSON")
    obj_place = request.get_json()
    if "name" not in obj_place:
        abort(400, "Missing name")
    obj_place["state_id"] = city_id

    new_place = City(**obj_place)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def updates_place(place_id):
    """ Update place """
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    up_place = models.storage.get(Place, place_id)
    if up_place is None:
        abort(404)
    obj_place = request.get_json()
    if obj_place is None:
        abort(400, 'Not a JSON')
    for k, v in obj_place.items():
        if k not in ['id', 'city_id', 'user_id', 'updated_at',
                       'created_at']:
            setattr(up_place, k, v)
    up_place.save()
    return jsonify(up_place.to_dict()), 200
