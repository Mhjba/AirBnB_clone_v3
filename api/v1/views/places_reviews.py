#!/usr/bin/python3
""" Handles everything related to reviews """

from models import storage
from models.review import Review
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route("/places/<place_id>/reviews", methods=['GET'])
def get_review_by_place(place_id):
    """Retrieves by id"""
    req_place = storage.get("Place", place_id)
    if not req_place:
        abort(404)
    return jsonify([r.to_dict() for r in req_place.reviews])


@app_views.route("/reviews/<review_id>", methods=['GET'])
def get_review_by_id(review_id):
    """
    Reyrieves a review by id
    """
    req_review = storage.get("Review", review_id)
    if not req_review:
        abort(404)
    return jsonify(req_review.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review_by_id(review_id):
    """
    Delete a review with the given id
    """
    req_review = storage.get("Review", review_id)
    if not req_review:
        abort(404)
    storage.delete(req_review)
    storage.save()
    return jsonify({}), 200
