#!/usr/bin/python3
"""
view for State objects that handles all default RESTFul API actions
"""
from flask import jsonify, abort, request, Blueprint
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_states():
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])
