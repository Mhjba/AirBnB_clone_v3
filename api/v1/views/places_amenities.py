#!/usr/bin/python3
""" place_amenity """
from flask import jsonify, abort

from api.v1.views import app_views
from models.place import Place
from models import storage
from models import storage_t as storage_type
from models.amenity import Amenity


@app_views.route("/places/<place_id>/amenities")
def get_place_amenity(place_id):
    """ get amenities place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    result = []
    if storage_type == "db":
        for amenity in place.amenities:
            result.append(amenity.to_dict())
    else:
        result = place.amenities

    return jsonify(result)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"])
def delete_place_amenity(place_id, amenity_id):
    """ delete amenity place """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place:
        abort(404)
    if not amenity:
        abort(404)
    if amenity not in place.amenities:
        abort(404)

    if storage_type == "db":
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity)
    storage.save()

    return jsonify({})


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"])
def link_place_amenity(place_id, amenity_id):
    """" Retrieves a Amenity object """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place:
        abort(404)
    if not amenity:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict())
    if storage_type == "db":
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity.id)
    storage.save()
    return jsonify(amenity.to_dict()), 201
