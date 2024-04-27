#!/usr/bin/python3
"""
Module for handling HTTP requests related to User objects
"""

import json
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/users', methods=['GET'])
def list_users():
    '''Retrieves a list of all User objects'''
    list_users = [obj.to_dict() for obj in storage.all("User").values()]
    return jsonify(list_users)


@app_views.route("/users/<user_id>", methods=['GET'])
def get_user(user_id):
    """Get one user
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete an user by id
    """
    result = storage.get(User, user_id)
    if result is None:
        abort(404)
    storage.delete(result)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'])
def create_user():
    """
    Create a new user
    """
    if not request.is_json:
        abort(400, description="Not a JSON")
    result = request.get_json()

    if "password" not in result:
        abort(400, description="Missing password")
    if "email" not in result:
        abort(400, description="Missing email")

    new_user = User(**result)
    storage.new(new_user)
    storage.save()
    return new_user.to_dict(), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def updates_user(user_id):
    """
    Update an user by id
    """
    result = storage.get(User, user_id)
    if not result:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")

    json_file = request.get_json()
    for x, y in json_file.items():
        if x != "id" and x != "updated_at" and x != "created_at":
            setattr(result, x, y)
    storage.save()
    return result.to_dict(), 200
