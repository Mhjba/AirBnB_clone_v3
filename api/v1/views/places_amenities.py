#!/usr/bin/python3
""" place_amenity """
from flask import jsonify, abort
from api.v1.views import app_views
from models.place import Place
from models import storage
from models import storage_t as storage_type
from models.amenity import Amenity
import models


@app_views.route("/places/<place_id>/amenities")
def get_place_amenity(place_id):
    """ get amenities place """
    gt_place = models.storage.get(Place, place_id)
    if not gt_place:
        return abort(404)
    gets = []
    if storage_type == "db":
        for amenity in gt_place.amenities:
            gets.append(amenity.to_dict())
    else:
        gets = gt_place.amenities
    return jsonify(gets)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"])
def delete_place_amenity(place_id, amenity_id):
    """ delete amenity place """
    dl_place = models.storage.get(Place, place_id)
    amenity = models.storage.get(Amenity, amenity_id)
    if not dl_place:
        return abort(404)
    if not amenity:
        return abort(404)
    if amenity not in dl_place.amenities:
        return abort(404)
    if storage_type == "db":
        dl_place.amenities.remove(amenity)
    else:
        dl_place.amenity_ids.remove(amenity)
    models.storage.save()
    return jsonify({})


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"])
def list_place_amenity(place_id, amenity_id):
    """" Retrieves a Amenity object """
    lt_place = models.storage.get(Place, place_id)
    amenity = models.storage.get(Amenity, amenity_id)
    if not lt_place:
        return abort(404)
    if not amenity:
        abort(404)
    if amenity in lt_place.amenities:
        return jsonify(amenity.to_dict())
    if storage_type == "db":
        lt_place.amenities.append(amenity)
    else:
        lt_place.amenity_ids.append(amenity.id)
    models.storage.save()
    return jsonify(amenity.to_dict()), 201
