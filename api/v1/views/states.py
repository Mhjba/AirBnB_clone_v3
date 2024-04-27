#!/usr/bin/python3
""" state API """

import json
from models import storage
from models.state import State
from api.v1.views import app_views
from models.base_model import BaseModel
from flask import jsonify, request, abort


@app_views.route('/states/', methods=['GET'])
def list_states():
    """ Retrieves a list of all State objects """
    list_states = [obj.to_dict() for obj in storage.all("State").values()]
    return jsonify(list_states)


@app_views.route("/states/<string:state_id>", methods=['GET'])
def get_state(state_id):
    """ get a state by id """
    all_state = storage.get(State, state_id)
    if all_state is None:
        abort(404)
    return jsonify(all_state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """ delete a state by id """
    req_state = storage.get(State, state_id)
    if req_state is None:
        abort(404)
    storage.delete(req_state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=['POST'])
def create_state():
    """ create a new state """
    if not request.is_json:
        abort(400, description="Not a JSON")
    req_state = request.get_json()

    if "name" not in req_state:
        abort(400, description="Missing name")

    all_state = State(**req_state)
    storage.new(all_state)
    storage.save()
    return all_state.to_dict(), 201


@app_views.route("/states/<state_id>", methods=['PUT', 'GET'])
def update_state(state_id):
    """ Updates a State object """
    all_state = storage.get(State, state_id)

    if not all_state:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")
    req_state = request.get_json()

    for obj, v in req_state.items():
        if obj != "id" and obj != "updated_at" and obj != "created_at":
            setattr(all_state, obj, v)
    storage.save()
    return all_state.to_dict(), 200
