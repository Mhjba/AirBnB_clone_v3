#!/usr/bin/python3
"""
This file contains the Amenity module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity
from flasgger.utils import swag_from
import models


@app_views.route('/amenities/', methods=['GET'])
def list_amenities():
    """ get amenities  """
    all_amenity = [obj.to_dict() for obj in models.storage.all(Amenity).values()]
    return jsonify(all_amenity)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """ get amenity """
    all_amenity = models.storage.get(Amenity, amenity_id)
    if all_amenity is None:
        abort(404)
    return jsonify(all_amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """ delete amenity """
    all_amenity = models.storage.get(Amenity, amenity_id)
    if all_amenity is None:
        abort(404)
    all_amenity.delete()
    models.storage.save()
    return jsonify({})


@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    """ create new amenity """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    amenity = request.get_json()
    all_amenity = Amenity(**amenity)
    all_amenity.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def updates_amenity(amenity_id):
    """  """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
