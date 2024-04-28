#!/usr/bin/python3
""" state API """

import json
from models import storage
from models.state import State
from api.v1.views import app_views
from models.base_model import BaseModel
from flask import Blueprint, jsonify, request, abort


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_all_states():
    """ returns all states """
    lt_states = [obj.to_dict() for obj in storage.all("State").values()]
    return jsonify(lt_states)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """ get state  """
    gt_state = storage.get(State, state_id)
    if gt_state is None:
        abort(404)
    return jsonify(gt_state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ delete state """
    dl_state = models.storage.get(State, state_id)
    if dl_state is None:
        abort(404)
    storage.delete(dl_state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'])
def create_state():
    """ create state """
    if not request.is_json:
        abort(400, description="Not a JSON")
    ct_json = request.get_json()

    if "name" not in ct_json:
        abort(400, description="Missing name")

    objs_state = State(**ct_json)
    storage.new(objs_state)
    storage.save()
    return objs_state.to_dict(), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def updates_state(state_id):
    """ Updates state """
    up_state = models.storage.get(State, state_id)
    if not up_state:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    state_json = request.get_json()
    for x, y in state_json.items():
        if x != "id" and x != "updated_at" and x != "created_at":
            setattr(up_state, x, y)
    storage.save()
    return up_state.to_dict(), 200
