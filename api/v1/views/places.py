#!/usr/bin/python3
"""Places module"""

from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.place import Place
from api.v1.views import app_views
from models.base_model import BaseModel


@app_views.route(
                    '/cities/<city_id>/places',
                    methods=['GET'],
                    strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route(
                    '/places/<place_id>',
                    methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
                    '/places/<place_id>',
                    methods=['DELETE'],
                    strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route(
                    '/cities/<city_id>/places',
                    methods=['POST'],
                    strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    user_id = data.get('user_id')
    if not user_id:
        abort(400, 'Missing user_id')
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    name = data.get('name')
    if not name:
        abort(400, 'Missing name')
    new_place = Place(name=name, city_id=city_id, user_id=user_id)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route(
                    '/places/<place_id>',
                    methods=['PUT'],
                    strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route(
                    '/places_search', methods=['POST'],
                    strict_slashes=False)
def search_places():
    """Search for places based on JSON parameters"""
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])
    if not states and not cities and not amenities:
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])
    places = []
    if states:
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    places.extend(city.places)
    if cities:
        for city_id in cities:
            city = storage.get(City, city_id)
            if city and city not in places:
                places.extend(city.places)
    if amenities:
        filtered_places = []
        for place in places:
            place_amenities = [amenity.id for amenity in place.amenities]
            if set(amenities).issubset(set(place_amenities)):
                filtered_places.append(place)
        places = filtered_places
    return jsonify([place.to_dict() for place in places])
