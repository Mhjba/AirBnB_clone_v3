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
def get_amenities():
    """ get amenities by id """
    all_list = []
    for k, v in storage.get(Amenity.items()):
        all_list.append(v.to_dict())
    return jsonify(all_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """ get amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """ delete amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        amenity.delete()
        storage.save()
        return jsonify({}),200
    else:
        abort(404)



@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    """ create new instance """
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    if request.get_json():
        abort(400, "Not a JSON")
    new_city = request.get_json()
    if 'name' not in new_city:
        abort(400, "Missing name")
    new_city = Amenity(**new_city)
    new_city.save()
    return jsonify(new_city.to_dict()), 200


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def updates_amenity(amenity_id):
    """  """
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    if not request.get_json():
        abort(400, "Not a JSON")
    obj_amen = request.get_json()
    Amenity = storage.get(Amenity, amenity_id)
    if Amenity:
        new_Amen = ['id', 'created_at', 'updated_at']
        for k, v in obj_amen.items():
            if k not in new_Amen:
                setattr(Amenity, k, v)
        Amenity.save()
        return jsonify(Amenity.to_dict())
