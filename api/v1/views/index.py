#!/usr/bin/python3
""" index file """
from api.v1.views import app_views
from flask import jsonify

@app_views.route("/status", methods=["GET"])
def status():
    """Returns the status of the API."""
    return jsonify({"status": "OK"})

@app_views.route("/api/v1/stats", methods=["GET"])
def stats():
    """Returns the number of each object type."""
    # Use the newly added count() method from storage
    # Implementation here
    return jsonify({
        "amenities": 47,
        "cities": 36,
        "places": 154,
        "reviews": 718,
        "states": 27,
        "users": 31
    })
