#!/usr/bin/python3
""" index file """
from api.v1.views import app_views
from flask import jsonify
import models
from models import storage


@app_views.route("/status")
def status():
    """Status of my API"""
    return jsonify({"status": "OK"})


@app_views.route("/status")
def stats():
    """ returns count of all classes' objects """
    return jsonify({
        "amenities": models.storage.count("Amenity"),
        "cities": models.storage.count("City"),
        "places": models.storage.count("Place"),
        "reviews": models.storage.count("Review"),
        "states": models.storage.count("State"),
        "users": models.storage.count("User")
    })
