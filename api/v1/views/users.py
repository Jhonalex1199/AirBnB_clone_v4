#!/usr/bin/python3
""" Amenity """
from os import getenv
from flask import Flask, jsonify, Blueprint, make_response, request, abort
from models import storage
from api.v1.views import app_views
from models.state import State
from models.user import User
ms1 = ['GET', 'POST']
ms2 = ['GET', 'DELETE', 'PUT']


@app_views.route('/users', strict_slashes=False, methods=ms1)
@app_views.route('/users/<user_id>', strict_slashes=False, methods=ms2)
def users_routes(user_id=None):
    """Amenities_routes"""
    objs = storage.all('User')
    if user_id:
        key = "User." + user_id
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
                if k not in ['id', 'email', 'created_at', 'updated_at']:
                    setattr(obj, k, v)
            storage.save()
            return make_response(jsonify(obj.to_dict()), 200)
    else:
        if request.method == 'POST':
            if not request.get_json():
                return jsonify({"error": "Not a JSON"}), 400
            data = request.get_json()
            if 'email' not in data.keys():
                return jsonify({"error": "Missing email"}), 400
            if 'password' not in data.keys():
                return jsonify({"error": "Missing password"}), 400
            new_user = User(**data)
            storage.new(new_user)
            storage.save()
            return make_response(jsonify(new_user.to_dict()), 201)
        user_list = []
        for obj in objs.values():
            user_list.append(obj.to_dict())
        return jsonify(user_list)
