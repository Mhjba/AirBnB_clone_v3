#!/usr/bin/python3
""" state """

import json
from models import storage
from models.state import State
from api.v1.views import app_views
from models.base_model import BaseModel
from flask import Blueprint, jsonify, request, abort
import models


@app_views.route("/states", methods=["GET"])
def all_states():
    """ get all states """
    all_states = [obj.to_dict() for obj in storage.all("State").values()]
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """ get state """
    gt_state = models.storage.get(State, state_id)
    if gt_state is None:
        return abort(404)
    return jsonify(gt_state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ delete state """
    dl_state = models.storage.get(State, state_id)
    if dl_state is None:
        return abort(404)
    models.storage.delete(dl_state)
    models.storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'])
def create_state():
    """ create state """
    if not request.is_json:
        return abort(400, description="Not a JSON")
    js = request.get_json()
    if "name" not in js:
        return abort(400, description="Missing name")
    cr_state = State(**js)
    models.storage.new(cr_state)
    models.storage.save()
    return cr_state.to_dict(), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def updates_state(state_id):
    """ Updates state info """
    up_state = models.storage.get(State, state_id)

    if not up_state:
        return abort(404)
    if not request.is_json:
        return abort(400, description="Not a JSON")
    js = request.get_json()
    for key, value in js.items():
        if key != "id" and key != "updated_at" and key != "created_at":
            setattr(up_state, key, value)
    models.storage.save()
    return up_state.to_dict(), 200
