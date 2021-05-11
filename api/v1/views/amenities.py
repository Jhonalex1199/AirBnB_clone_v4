#!/usr/bin/python3
""" Amenity """
from os import getenv
from flask import Flask, jsonify, Blueprint, make_response, request, abort
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity

ms1 = ['GET', 'POST']
ms2 = ['GET', 'DELETE', 'PUT']


@app_views.route('/amenities', strict_slashes=False, methods=ms1)
@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=ms2)
def amenities_routes(amenity_id=None):
    """Amenities_routes"""
    objs = storage.all('Amenity')
    if amenity_id:
        key = "Amenity." + amenity_id
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
                return ('Not a JSON'), 400
            data = request.get_json()
            for k, v in data.items():
                if k not in ['id', 'created_at', 'updated_at']:
                    setattr(obj, k, v)
            storage.save()
            return make_response(jsonify(obj.to_dict()), 200)
    else:
        if request.method == 'POST':
            if not request.get_json():
                return ('Not a JSON'), 400
            data = request.get_json()
            if 'name' not in data.keys():
                return ('Missing name'), 400
            new_amenity = Amenity(**data)
            storage.new(new_amenity)
            storage.save()
            return make_response(jsonify(new_amenity.to_dict()), 201)
        amenities_list = []
        for obj in objs.values():
            amenities_list.append(obj.to_dict())
        return jsonify(amenities_list)
