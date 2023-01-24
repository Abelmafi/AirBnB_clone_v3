#!/usr/bin/python3
"""Creating restful api module"""

from api.v1.views import app_views
from models.base_model import BaseModel
from flask import Flask, jsonify, abort, request
from models import storage


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def users(user_id=None):
    """User RESTFul API"""
    from models.user import User
    user_obj = storage.all(User)

    if request.method == 'GET':
        if user_id:
            ids = [key.split('.')[1] for key in user_obj]
            if user_id not in ids:
                abort(404)
            else:
                key = 'User.' + user_id
                return (user_obj[key].to_dict())
        else:
            return jsonify([value.to_dict() for value in user_obj.values()])

    elif request.method == 'POST':
        user_json = request.get_json()
        if request.is_json:
            if 'email' not in user_json:
                abort(400)
            elif 'password' not in user_json:
                abort(400)
            else:
                new_user = User(**user_json)
                storage.new(new_user)
                storage.save()
                return (new_user.to_dict()), 201
        else:
            abort(400, 'Not a JSON')

    elif request.method == 'DELETE':
        ids = [key.split('.')[1] for key in user_obj]

        if user_id in ids:
            key = "User." + user_id
            storage.delete(user_obj[key])
            storage.save()
            return {}, 200
        else:
            abort(404)

    elif request.method == 'PUT':
        ids = [key.split('.')[1] for key in user_obj]

        if user_id in ids:
            key = 'User.' + user_id
            target_obj = user_obj[key]
            user_json = request.get_json()
            if not request.is_json:
                abort(400, 'Not a JSON')
            else:
                for key, value in user_json.items():
                    if key not in ['id', 'email', 'created_at', 'updated_at']:
                        setattr(target_obj, key, value)
                storage.save()
                return (target_obj.to_dict()), 200
        else:
            abort(404)

    else:
        abort(501)
