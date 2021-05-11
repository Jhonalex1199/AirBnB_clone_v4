#!/usr/bin/python3
"""State"""
from os import getenv
from flask import Flask, jsonify, Blueprint, make_response, request, abort
from models import storage
from api.v1.views import app_views
from models.state import State


mets = ['GET', 'POST']
mets_id = ['GET', 'DELETE', 'PUT']


@app_views.route('/states', strict_slashes=False, methods=mets)
@app_views.route('/states/<state_id>', strict_slashes=False, methods=mets_id)
def states_routes(state_id=None):
    """States_routes"""
    objs = storage.all('State')
    if state_id:
        key = "State." + state_id
        obj = objs.get(key)
        if obj is None:
            abort(404)
        if request.method == 'GET':
            return jsonify(obj.to_dict())
        elif request.method == 'DELETE':
            storage.delete(obj)
            storage.save()
            return make_response(jsonify({}), 200)
        elif request.method == 'PUT':
            if not request.get_json():
                return jsonify({"error": "Not a JSON"}), 400
            data = request.get_json()
            for k, v in data.items():
                if k not in ['created_at', 'updated_at']:
                    setattr(obj, k, v)
            storage.save()
            return make_response(jsonify(obj.to_dict()), 200)
    else:
        if request.method == 'POST':
            if not request.get_json():
                return ('Not a JSON'), 400
            data = request.get_json()
            if 'name' not in data.keys():
                return jsonify({"error": "Missing name"}), 400
            new_state = State(**data)
            storage.new(new_state)
            storage.save()
            return make_response(jsonify(new_state.to_dict()), 201)
        states_list = []
        for obj in objs.values():
            states_list.append(obj.to_dict())
        return jsonify(states_list)
