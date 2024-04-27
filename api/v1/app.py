#!/usr/bin/python3
""" Application """
from flask import Flask, Blueprint, jsonify
from api.v1.views import app_views
from models import storage
from flask_cors import CORS
from os import getenv
import models

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_app(e):
    """ closes storage engine """
    models.storage.close()


@app.errorhandler(404)
def not_found(err):
    """ handles 404 error and gives json formatted response """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=getenv("HBNB_API_PORT", "5000"), threaded=True)
