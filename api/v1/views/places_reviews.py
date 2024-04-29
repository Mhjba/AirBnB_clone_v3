#!/usr/bin/python3
""" places reviews """

from models import storage
from models.review import Review
from api.v1.views import app_views
from flask import abort, jsonify, request
import models


@app_views.route("/places/<place_id>/reviews", methods=['GET'])
def get_place_reviewe(place_id):
    """ get place reviewe """
    gt_place = models.storage.get("Place", place_id)
    if not gt_place:
        return abort(404)
    return jsonify([pc.to_dict() for pc in gt_place.reviews])


@app_views.route("/reviews/<review_id>", methods=['GET'])
def get_review(review_id):
    """ get review """
    gt_review = models.storage.get("Review", review_id)
    if not gt_review:
        return abort(404)
    return jsonify(gt_review.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'])
def delete_review(review_id):
    """ Delete review """
    dl_review = models.storage.get("Review", review_id)
    if not dl_review:
        return abort(404)
    models.storage.delete(dl_review)
    models.storage.save()
    return jsonify({}), 200
