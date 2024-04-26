#!/usr/bin/python3
"""Routes Handling for the App.

This module contains route handlers for the Flask app.
It defines the various routes and their corresponding functions
to handle incoming HTTP requests.
Each route is responsible for a specific endpoint or functionality of the app.

Routes:
- GET /status: Returns the status of the API.
- GET /stats: Retrieves the number of each object by type.
"""

from api.v1.views import app_views
from flask import Response, jsonify
from models import storage
from models.engine.db_storage import classes


@app_views.route("/status")
def check_status():
    """Returns the status of the API."""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def num_objs():
    """Retrieves the number of each objects by type."""
    objects = {
        "amenities": storage.count(classes["Amenity"]),
        "cities": storage.count(classes["City"]),
        "places": storage.count(classes["Place"]),
        "reviews": storage.count(classes["Review"]),
        "states": storage.count(classes["State"]),
        "users": storage.count(classes["User"]),
    }
    return jsonify(objects)
