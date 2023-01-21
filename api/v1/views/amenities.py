#!/usr/bin/python3
"""Creates a RESTFul API for Amenity"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.base_model import BaseModel


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def amenity(amenity_id=None):
    """Amenity RESTFul API"""
    from models.amenity import Amenity
    amenity_obj = storage.all(Amenity)

    if request.method == 'GET':
        return jsonify([value.to_dict() for key, value in amenity_obj.items()])

    elif request.method == 'POST':
        amenity_json = request.get_json()
        if request.is_json:
            if 'name' in amenity_json:
                new_amenity = Amenity(**amenity_json)
                storage.new(new_amenity)
                storage.save()
                return (new_amenity.to_dict()), 201

            else:
                abort(400)
        else:
            abort(400, 'Not a JSON')

    elif request.method == 'DELETE':
        ids = [key.split('.')[1] for key in amenity_obj]

        if amenity_id in ids:
            key = "Amenity." + amenity_id
            storage.delete(amenity_obj[key])
            storage.save()
            return {}, 200
        else:
            abort(404)

    elif request.method == 'PUT':
        ids = [key.split('.')[1] for key in amenity_obj]

        if amenity_id in ids:
            key = 'Amenity.' + amenity_id
            target_obj = amenity_obj[key]
            amenity_json = request.get_json()
            if request.is_json:
                for key, value in amenity_json.items():
                    if key not in ['id', 'created_at', 'updated_at']:
                        setattr(target_obj, key, value)
                storage.save()
                return (target_obj.to_dict()), 200

            else:
                abort(400, 'Not a JSON')
        else:
            abort(404)
