#!/usr/bin/python3
"""Creating restfull api"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.base_model import BaseModel


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def city_place(city_id=None):
    """Creating RESTFul api"""
    from models.city import City
    from models.place import Place
    city_obj = storage.all(City)
    place_obj = storage.all(Place)
    user_obj = storage.all(User)

    if request.method == 'GET':
        ids = [key.split('.')[1] for key in city_obj]
        if city_id in ids:
            return [value.to_dict() for value in place_obj.values()
                    if value.to_dict()['city_id'] == city_id]
        else:
            abort(404)

    elif request.method == 'POST':
        c_ids = [key.split('.')[1] for key in city_obj]
        if city_id in c_ids:
            content_type = request.headers.get('Content-Type')
            if content_type == 'application/json':
                body_json = request.get_json()
                if 'user_id' not in body_json:
                    abort(400, 'Missing user_id')
                elif 'name' not in body_json:
                    abort(400, 'Missing name')
                else:
                    u_ids = [key.split('.')[1] for key in user_obj]
                    if ('User.' + body_json['user_id']) not in user_obj.keys():
                        abort(404)
                    else:
                        body_json.update({'city_id': city_id})
                        new_place = Place(**body_json)
                        storage.new(new_place)
                        storage.save()
                        return (new_place.to_dict()), 201
            else:
                abort(400, 'Not a JSON')
        else:
            abort(404)
    else:
        abort(501)


@app_views.route('/places', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def places(place_id=None):
    """Creates State objects that handles all default RESTFul API"""

    from models.place import Place
    place_obj = storage.all(Place)

    if request.method == 'GET':
        if place_id is None:
            return jsonify([obj.to_dict() for obj in place_obj.values()])
        key = 'Place.' + place_id
        try:
            return jsonify(place_obj[key].to_dict())
        except Exception:
            abort(404)

    elif request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            abort(400, 'Not a JSON')
        else:
            body_json = request.get_json()
            if 'name' not in body_json:
                abort(400, 'Missing name')
            else:
                new_place = Place(**body_json)
                storage.new(new_place)
                storage.save()
                return jsonify(new_place.to_dict()), 201

    elif request.method == 'PUT':
        ids = [key.split('.')[1] for key in place_obj]
        if place_id not in ids:
            abort(404)
        else:
            key = 'Place.' + place_id
            found_place = place_obj[key]
            content_type = request.headers.get('Content-Type')
            if content_type == 'application/json':
                body_json = request.get_json()
                ign = ['city_id', 'user_id', 'created_at', 'updated_at', 'id']
                for key, value in body_json.items():
                    if key not in ign:
                        setattr(found_place, key, value)
                storage.save()
                return jsonify(found_place.to_dict()), 200
            else:
                abort(400, 'Not a JSON')

    elif request.method == 'DELETE':
        key = 'Place.' + place_id
        ids = [val.split('.')[1] for val in place_obj]
        if place_id not in ids:
            abort(404)
        else:
            storage.delete(place_obj[key])
            storage.save()
            return {}, 200

    else:
        abort(501)
