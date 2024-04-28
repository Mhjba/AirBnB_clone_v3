#!/usr/bin/python3
""" Handles everything related to places """

from models import storage
from models.city import City
from models.state import State
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route("/cities/<string:city_id>/places", methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """
    Retrieve all places by city id given
    """
    city = storage.get(City, city_id)
    if not city:
        return abort(404)
    places = [place.t_dict() for place in city.places]
    return jsonify(places)


@app_views.route("/places/<string:place_id>", methods=['GET'],
                 strict_slashes=False)
def get_place_by_id(place_id):
    """
    Reyrieves a place by id
    """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        return abort(404)  


@app_views.route("/places/<string:place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_place_by_id(place_id):
    """
    Delete a place by id
    """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_new_place(city_id):
    """
    Create a new place
    """
    city = storage.get(City, city_id)
    if not city:
        return abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing user_id')
    user = storage.get("User", data['user_id'])
    if not user:
        return abort(404)
    data['city_id'] = city_id
    place = place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place_by_id(place_id):
    """
    Update an place by id
    """
    place = storage.get(Place, place_id)
    if place:
        if not request.get_json():
            abort(400, 'Not a JSON')
        data = request.get_json()
        ignor = ['id', 'city_id', 'user_id', 'updated_at', 'created_at']
        for k, v in data.items():
            if k not in ignor:
                setattr(place, k, v)
        place.save()
        return jsonify(place.to_dict()), 200
    else:
        return abort(404)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Handles search feature in places
    """
    if request.get_json() is None:
        abort(400, description="Not a JSON")

    req_json = request.get_json()

    if req_json and len(req_json):
        req_states = req_json.get('states', None)
        req_cities = req_json.get('cities', None)
        req_amenities = req_json.get('amenities', None)

    if not req_json or not len(req_json) or (
            not req_states and
            not req_cities and
            not req_amenities):
        places = storage.all(Place).values()
        place_arr = [place.to_dict() for place in places]
        return jsonify(place_arr)

    place_arr = []
    if req_states:
        get_s = [storage.get(State, state_id) for state_id in req_states]
        for state in get_s:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            place_arr.append(place)

    if req_cities:
        get_c = [storage.get(City, city_id) for city_id in req_cities]
        for city in get_c:
            if city:
                for place in city.places:
                    if place not in place_arr:
                        place_arr.append(place)

    if req_amenities:
        if not place_arr:
            place_arr = storage.all(Place).values()
        amen = [storage.get(Amenity, amenity_id)
                for amenity_id in req_amenities]
        place_arr = [place for place in place_arr
                     if all([idx in place.amenities
                            for idx in amen])]

    res = []
    for place in place_arr:
        place_dict = place.to_dict()
        place_dict.pop('amenities', None)
        res.append(place_dict)

    return jsonify(res)
