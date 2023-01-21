#!/usr/bin/python3
"""Creating restfull api"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.base_model import BaseModel


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def states(state_id=None):
    """Creates State objects that handles all default RESTFul API"""

    from models.state import State
    state_obj = storage.all(State)

    if request.method == 'GET':
        if state_id is None:
            return jsonify([obj.to_dict() for obj in state_obj.values()])
        key = 'State.' + state_id
        try:
            return jsonify(state_obj[key].to_dict())
        except Exception:
            abort(404)

    elif request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            body_json = request.get_json()
        else:
            abort(400, 'Not a JSON')

        if 'name' in body_json:
            new_state = State(**body_json)
            storage.new(new_state)
            storage.save()
            return jsonify(new_state.to_dict()), 201
        else:
            abort(400, 'Missing name')

    elif request.method == 'PUT':
        ids = [key.split('.')[1] for key in state_obj]
        if state_id in ids:
            key = 'State.' + state_id
            found_state = state_obj[key]
            content_type = request.headers.get('Content-Type')
            if content_type == 'application/json':
                body_json = request.get_json()
                for key, value in body_json.items():
                    if key not in ['created_at', 'updated_at', 'id']:
                        found_state.setattr(state_obj, key, value)
                storage.save()
            else:
                abort(400, 'Not a JSON')
        else:
            abort(404)

    elif request.method == 'DELETE':
        key = 'State.' + state_id
        ids = [val.split('.')[1] for val in state_obj]
        if state_id in ids:
            storage.delete(state_obj[key])
            storage.save()
            return {}, 200

        else:
            abort(404)
