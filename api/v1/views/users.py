#!/usr/bin/python3
""" Users """

import json
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, abort
import models


@app_views.route('/users', methods=['GET'])
def list_users():
    """ Get all users """
    all_users = [obj.to_dict() for obj in models.storage.all("User").values()]
    return jsonify(all_users)


@app_views.route("/users/<user_id>", methods=['GET'])
def get_user(user_id):
    """ Get User id """
    all_user = models.storage.get(User, user_id)
    if not all_user:
        abort(404)
    return jsonify(all_user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ Deletes a User id """
    all_user = models.storage.get(User, user_id)
    if all_user is None:
        abort(404)
    models.storage.delete(all_user)
    models.storage.save()
    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'])
def create_user():
    """ Creates a User """
    if not request.is_json:
        abort(400, "Not a JSON")
    all_user = request.get_json()
    if "password" not in all_user:
        abort(400, "Missing password")
    if "email" not in all_user:
        abort(400, "Missing email")
    new_user = User(**all_user)
    models.storage.new(new_user)
    models.storage.save()
    return new_user.to_dict(), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def updates_user(user_id):
    """ Update an user id """
    all_user = models.storage.get(User, user_id)
    if not all_user:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")

    user_obj = request.get_json()
    for objs, v in user_obj.items():
        if objs != "id" and objs != "updated_at" and objs != "created_at":
            setattr(all_user, objs, v)
    models.storage.save()
    return all_user.to_dict(), 200
