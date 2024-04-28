#!/usr/bin/python3
"""
This file contains the Amenity module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity
from flasgger.utils import swag_from


@app_views.route('/amenities/', methods=['GET'])
def list_amenities():
    """ get amenities by id """
    all_list = [obj.to_dict() for obj in storage.all(Amenity).values()]
    return jsonify(all_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """ get amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """ delete amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    """ create new instance """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    js = request.get_json()
    obj = Amenity(**js)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def update_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    payload = request.get_json()
    if not amenity:
        abort(404)
    if not payload:
        abort(400, "Not a JSON")

    key = "name"
    setattr(amenity, key, payload[key])
    amenity.save()

    return jsonify(amenity.to_dict()), 200
