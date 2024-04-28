#!/usr/bin/python3
""" state API """

import json
from models import storage
from models.state import State
from api.v1.views import app_views
from models.base_model import BaseModel
from flask import Flask, Blueprint, jsonify, request, url_for, abort


@app_views.route('/states/', methods=['GET'])
def list_states():
    """ returns all states """
    states = storage.all(State).values()
    states_json = []

    for state in states:
        states_json.append(state.to_dict())
    return jsonify(states_json)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """ get a state by id """
    req_state = storage.get(State, state_id)
    if req_state is None:
        abort(404)
    return jsonify(req_state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ delete a state by id """
    req_state = storage.get(State, state_id)
    if req_state is None:
        abort(404)
    storage.delete(req_state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'])
def create_state():
    """ create a new state """
    if not request.is_json:
        abort(400, description="Not a JSON")
    state_json = request.get_json()

    if "name" not in state_json:
        abort(400, description="Missing name")

    new_state = State(**state_json)
    storage.new(new_state)
    storage.save()
    return new_state.to_dict(), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def updates_state(state_id):
    """ Updates state info """
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")
    state_json = request.get_json()

    for x, y in state_json.items():
        if x != "id" and x != "updated_at" and x != "created_at":
            setattr(state, x, y)
    storage.save()
    return state.to_dict(), 200
