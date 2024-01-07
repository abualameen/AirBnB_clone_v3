#!/usr/bin/python3
"""This module handles all default RESTFul API actions for State objects."""
from flask import jsonify, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views
from models.base_model import BaseModel


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Retrieves the list of all State objects."""
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    """Retrieves a State object."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State."""
    json_data = request.get_json()
    print("json_data", json_data)
    if not json_data:
        abort(400, description="Not a JSON")
    if 'name' not in json_data:
        abort(400, description="Missing name")
    new_state = State(**json_data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        abort(400, description="Not a JSON")
    for key, value in json_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    
    # Utilize the storage system's delete method here.
    storage.delete(state)
    storage.save()  # Ensure changes are committed to the database
    
    return jsonify({}), 200