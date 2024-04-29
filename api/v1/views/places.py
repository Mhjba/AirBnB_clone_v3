#!/usr/bin/python3
""" places """

from models import storage
from models.city import City
from models.state import State
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from flask import abort, jsonify, request
import models


@app_views.route("/cities/<string:city_id>/places", methods=['GET'])
def get_places_city(city_id):
    """ get all places """
    gt_city = models.storage.get(City, city_id)
    if gt_city is None:
        abort(404)
    places = gt_city.places
    all_places = []
    for item in places:
        all_places.append(item.to_dict())
    return jsonify(all_places)


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
    cr_place = models.storage.get(City, city_id)
    if cr_place is None:
        return abort(404)
    obj_place = request.get_json()
    if obj_place is None:
        return abort(400, 'Not a JSON')
    if 'user_id' not in obj_place:
        return abort(400, 'Missing user_id')
    user = models.storage.get("User", obj_place['user_id'])
    if user is None:
        abort(404)
    if 'name' not in obj_place:
        return abort(400, 'Missing name')
    obj_place['city_id'] = city_id
    places = Place(**obj_place)
    places.save()
    return jsonify(places.to_dict()), 201
