#!/usr/bin/python3
""" Amenity """
from os import getenv
from flask import Flask, jsonify, Blueprint, make_response, request, abort
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User


me = ['GET', 'POST']
mets_id = ['GET', 'DELETE', 'PUT']


@app_views.route('/places/<place_id>', strict_slashes=False, methods=mets_id)
def places_routes(place_id=None):
    """ Places_routes """
    objs = storage.all('Place')
    if place_id:
        key = "Place." + place_id
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
            try:
                data = request.get_json()
            except Exception:
                return jsonify({"error": "Not a JSON"}), 400
            if data is None:
                return jsonify({"error": "Not a JSON"}), 400
            attrs = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
            for k, v in data.items():
                if k not in attrs:
                    setattr(obj, k, v)
            storage.save()
            return make_response(jsonify(obj.to_dict()), 200)


@app_views.route('/cities/<city_id>/places', strict_slashes=False, methods=me)
def places_routes2(city_id=None):
    """ Places_routes """
    objs_city = storage.all('City')
    objs_users = storage.all('User')
    all_places = []
    if city_id:
        key = "City." + city_id
        obj = objs_city.get(key)
        if obj is None:
            abort(404)
        if request.method == 'GET':
            for plc in obj.places:
                all_places.append(plc.to_dict())
            return jsonify(all_places)
        elif request.method == 'POST':
            try:
                data = request.get_json()
            except Exception:
                return jsonify({"error": "Not a JSON"}), 400
            if data is None:
                return jsonify({"error": "Not a JSON"}), 400
            if 'user_id' not in data.keys():
                return jsonify({"error": "Missing user_id"}), 400
            key_usr = "User." + data['user_id']
            obj_user = objs_users.get(key_usr)
            if obj_user is None:
                abort(404)
            if 'name' not in data.keys():
                return jsonify({"error": "Missing name"}), 400
            data['city_id'] = city_id
            new_place = Place(**data)
            storage.new(new_place)
            storage.save()
            return make_response(jsonify(new_place.to_dict()), 201)
