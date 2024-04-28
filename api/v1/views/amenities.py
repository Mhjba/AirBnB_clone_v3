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
    """ list of amenities """
    lt_amenities = [obj.to_dict() for obj in models.storage.all("Amenity").values()]
    return jsonify(lt_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """ get amenity """
    gt_amenity = models.storage.get(Amenity, amenity_id)
    if gt_amenity is None:
        abort(404)
    return jsonify(gt_amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """ delete amenity by id"""
    dl_amenity = models.storage.get(Amenity, amenity_id)
    if dl_amenity is None:
        abort(404)
    dl_amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    """ create new instance """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    amenity = request.get_json()
    cr_amenity = Amenity(**amenity)
    cr_amenity.save()
    return jsonify(cr_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def updates_amenity(amenity_id):
    """ updates amenity """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    up_amenity = models.storage.get(Amenity, amenity_id)
    if up_amenity is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(up_amenity, key, value)
    storage.save()
    return jsonify(up_amenity.to_dict())
