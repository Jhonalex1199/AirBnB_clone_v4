#!/usr/bin/python3
""" Places reviews """
from flask import Flask, jsonify, Blueprint, make_response, request, abort
from models import storage
from api.v1.views import app_views
from models.review import Review


m1 = ['GET', 'POST']
m2 = ['GET', 'DELETE', 'PUT']


@app_views.route('places/<place_id>/reviews', strict_slashes=False, methods=m1)
def places_reviews(place_id=None):
    """ Places_reviews routes """
    objs_places = storage.all('Place')
    all_revs = []
    if place_id:
        key_place = "Place." + place_id
        obj_place = objs_places.get(key_place)
        if obj_place is None:
            abort(404)
        if request.method == 'GET':
            for rev in obj_place.reviews:
                all_revs.append(rev.to_dict())
            return jsonify(all_revs)
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
            usr_objs = storage.all('User')
            usr_obj = usr_objs.get(key_usr)
            if usr_obj is None:
                abort(404)
            if 'text' not in data.keys():
                return jsonify({"error": "Missing text"}), 400
            data['place_id'] = place_id
            new_review = Review(**data)
            storage.new(new_review)
            storage.save()
            return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('reviews/<review_id>', strict_slashes=False, methods=m2)
def places_reviews2(review_id=None):
    """ Places_reviews_routes """
    all_revs = storage.all('Review')
    if review_id:
        key_rev = "Review." + review_id
        rev_obj = all_revs.get(key_rev)
        if rev_obj is None:
            abort(404)
        if request.method == 'GET':
            return jsonify(rev_obj.to_dict())
        elif request.method == 'DELETE':
            storage.delete(rev_obj)
            storage.save()
            return make_response(jsonify({}), 200)
        elif request.method == 'PUT':
            try:
                data = request.get_json()
            except Exception:
                return jsonify({"error": "Not a JSON"}), 400
            if data is None:
                return jsonify({"error": "Not a JSON"}), 400
            attrs = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
            for k, v in data.items():
                if k not in attrs:
                    setattr(rev_obj, k, v)
            storage.save()
            return make_response(jsonify(rev_obj.to_dict()), 200)
