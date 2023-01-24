#!/usr/bin/python3
"""Places view API request handlers
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.base_model import BaseModel


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def state_city(state_id=None):
    """Creating RESTFul api"""
    from models.city import City
    from models.state import State
    city_obj = storage.all(City)
    state_obj = storage.all(State)

    if request.method == 'GET':
        ids = [key.split('.')[1] for key in state_obj]
        if state_id in ids:
            return jsonify([value.to_dict() for value in city_obj.values()
                            if value.to_dict()['state_id'] == state_id])
        else:
            abort(404)

    elif request.method == 'POST':
        s_ids = [key.split('.')[1] for key in state_obj]
        if state_id in s_ids:
            content_type = request.headers.get('Content-Type')
            if content_type == 'application/json':
                body_json = request.get_json()
                if 'name' not in body_json:
                    abort(400, 'Missing name')
                else:
                    body_json.update({'state_id': state_id})
                    new_city = City(**body_json)
                    storage.new(new_city)
                    storage.save()
                    return (new_city.to_dict()), 201
            else:
                abort(400, 'Not a JSON')
        else:
            abort(404)
    else:
        abort(501)


@app_views.route('/cities', methods=['GET'], strict_slashes=False)
@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def cities(city_id=None):
    """Creates State objects that handles all default RESTFul API"""

    from models.city import City
    city_obj = storage.all(City)

    if request.method == 'GET':
        if city_id is None:
            return jsonify([obj.to_dict() for obj in city_obj.values()])
        key = 'City.' + city_id
        try:
            return jsonify(city_obj[key].to_dict())
        except Exception:
            abort(404)

    elif request.method == 'PUT':
        ids = [key.split('.')[1] for key in city_obj]
        if city_id not in ids:
            abort(404)
        else:
            key = 'City.' + city_id
            found_city = city_obj[key]
            content_type = request.headers.get('Content-Type')
            if content_type == 'application/json':
                body_json = request.get_json()
                ign = ['state_id', 'created_at', 'updated_at', 'id']
                for key, value in body_json.items():
                    if key not in ign:
                        setattr(found_city, key, value)
                storage.save()
                return jsonify(found_city.to_dict()), 200
            else:
                abort(400, 'Not a JSON')

    elif request.method == 'DELETE':
        key = 'City.' + city_id
        ids = [val.split('.')[1] for val in city_obj]
        if city_id not in ids:
            abort(404)
        else:
            storage.delete(city_obj[key])
            storage.save()
            return jsonify({}), 200
    else:
        abort(501)
