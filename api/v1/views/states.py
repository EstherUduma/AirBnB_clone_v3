#!/usr/bin/python3
"""
view for State objects that handles all default RESTFul API actions
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET', 'POST'])
def get_states():
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        if 'name' not in data:
            abort(400, 'Missing name')

        new_state = State(**data)
        new_state.save()

        return jsonify(new_state.to_dict()), 201
    else:
        states = storage.all(State).values()
        return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'])
def get_state_by_id(state_id):
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    if request.method == 'PUT':
        data = request.get_json()

        if not data:
            return jsonify({"error": "Not a JSON"}), 400

        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)

        storage.save()

        return jsonify(state.to_dict()), 200
    elif request.method == 'DELETE':
        state.delete()
        storage.save()
        return jsonify({}), 200
    
    return jsonify([state.to_dict()]), 200
