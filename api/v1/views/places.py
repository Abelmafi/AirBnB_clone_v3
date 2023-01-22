#!/usr/bin/python3
"""Places view API request handlers
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places_search',
                 methods=['POST'],
                 strict_slashes=False)
def places_search():
    """Search for place according to parameters
    in body request
    """
    # POST REQUEST
    if request.is_json:  # check is request is valid json
        body = request.get_json()
    else:
        abort(400, 'Not a JSON')

    place_list = []

    # if states searched
    if 'states' in body:
        for state_id in body['states']:
            state = storage.get(State, state_id)
            if state is not None:
                for city in state.cities:
                    for place in city.places:
                        place_list.append(place)

    # if cities searched
    if 'cities' in body:
        for city_id in body['cities']:
            city = storage.get(City, city_id)
            if city is not None:
                for place in city.places:
                    place_list.append(place)

    # if 'amenities' present
    if 'amenities' in body and len(body['amenities']) > 0:
        if len(place_list) == 0:
            place_list = [place for place in storage.all(Place).values()]
        del_list = []
        for place in place_list:
            for amenity_id in body['amenities']:
                amenity = storage.get(Amenity, amenity_id)
                if amenity not in place.amenities:
                    del_list.append(place)
                    break
        for place in del_list:
            place_list.remove(place)

    if len(place_list) == 0:
        place_list = [place for place in storage.all(Place).values()]

    # convert objs to dict and remove 'amenities' key
    place_list = [place.to_dict() for place in place_list]
    for place in place_list:
        try:
            del place['amenities']
        except KeyError:
            pass

    return jsonify(place_list)


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def places_by_city_requests(city_id):
    """Perform API requests of places by city
    """
    # GET REQUESTS
    if request.method == 'GET':
        # retrieve all places related to specific city, if exists
        cities = storage.all(City)
        try:
            key = 'City.' + city_id
            city = cities[key]
            place_list = [place.to_dict() for place in city.places]
            return jsonify(place_list)
        except KeyError:
            abort(404)

    # POST REQUESTS
    elif request.method == 'POST':
        # create a new place
        cities = storage.all(City)

        if ('City.' + city_id) not in cities.keys():
            abort(404)

        if request.is_json:  # check is request is valid json
            body_request = request.get_json()
        else:
            abort(400, 'Not a JSON')

        # check for required attributes
        if 'name' not in body_request:
            abort(400, 'Missing name')
        if 'user_id' not in body_request:
            abort(400, 'Missing user_id')

        # verify user_id is valid
        users = storage.all(User)
        if ('User.' + body_request['user_id']) not in users.keys():
            abort(404)

        # instantiate, store, and return new State object
        body_request.update({'city_id': city_id})
        new_place = Place(**body_request)
        storage.new(new_place)
        storage.save()
        return jsonify(new_place.to_dict()), 201

    # UNSUPPORTED REQUESTS
    else:
        abort(501)


@app_views.route('/places/<place_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place_methods(place_id=None):
    """Perform API requests of on place objects
    """
    # GET REQUESTS
    if request.method == 'GET':
        # retrieve specific place object, if exists
        places = storage.all(Place)
        try:
            key = 'Place.' + place_id
            place = places[key]
            return jsonify(place.to_dict())
        except KeyError:
            abort(404)

    # DELETE REQUESTS
    elif request.method == 'DELETE':

        # delete specific place, if exists
        places = storage.all(Place)
        try:
            key = 'Place.' + place_id
            storage.delete(places[key])
            storage.save()
            return jsonify({}), 200
        except KeyError:
            abort(404)

    # PUT REQUESTS
    elif request.method == 'PUT':
        places = storage.all(Place)
        key = 'Place.' + place_id
        try:
            place = places[key]

            # convert JSON request to dict
            if request.is_json:
                body_request = request.get_json()
            else:
                abort(400, 'Not a JSON')

            # update Place object
            ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
            for key, val in body_request.items():
                if key not in ignore:
                    setattr(place, key, val)

            storage.save()
            return jsonify(place.to_dict()), 200

        except KeyError:
            abort(404)

    # UNSUPPORTED REQUESTS
    else:
        abort(501)
# #usr/bin/python3
#"""Creating restfull api"""
#
#from api.v1.views import app_views
#from flask import Flask, jsonify, abort, request
#from models import storage
#from models.base_model import BaseModel
#
#
#@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
#                 strict_slashes=False)
#def city_place(city_id=None):
#    """Creating RESTFul api"""
#    from models.city import City
#    from models.place import Place
#    from models.user import User
#    city_obj = storage.all(City)
#    place_obj = storage.all(Place)
#    user_obj = storage.all(User)
#
#    if request.method == 'GET':
#        ids = [key.split('.')[1] for key in city_obj]
#        if city_id in ids:
#            return jsonify([value.to_dict() for value in place_obj.values()
#                    if value.to_dict()['city_id'] == city_id])
#        else:
#            abort(404)
#
#    elif request.method == 'POST':
#        c_ids = [key.split('.')[1] for key in city_obj]
#        if city_id in c_ids:
#            content_type = request.headers.get('Content-Type')
#            if content_type == 'application/json':
#                body_json = request.get_json()
#                if 'user_id' not in body_json:
#                    abort(400, 'Missing user_id')
#                elif 'name' not in body_json:
#                    abort(400, 'Missing name')
#                else:
#                    u_ids = [key.split('.')[1] for key in user_obj]
#                    if ('User.' + body_json['user_id']) not in user_obj.keys():
#                        abort(404)
#                    else:
#                        body_json.update({'city_id': city_id})
#                        new_place = Place(**body_json)
#                        storage.new(new_place)
#                        storage.save()
#                        return (new_place.to_dict()), 201
#            else:
#                abort(400, 'Not a JSON')
#        else:
#            abort(404)
#    else:
#        abort(501)
#
#
#@app_views.route('/places', methods=['GET'], strict_slashes=False)
#@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
#def places(place_id=None):
#    """Creates State objects that handles all default RESTFul API"""
#
#    from models.place import Place
#    place_obj = storage.all(Place)
#
#    if request.method == 'GET':
#        if place_id is None:
#            return jsonify([obj.to_dict() for obj in place_obj.values()])
#        key = 'Place.' + place_id
#        try:
#            return jsonify(place_obj[key].to_dict())
#        except Exception:
#            abort(404)
#
#    elif request.method == 'PUT':
#        ids = [key.split('.')[1] for key in place_obj]
#        if place_id not in ids:
#            abort(404)
#        else:
#            key = 'Place.' + place_id
#            found_place = place_obj[key]
#            content_type = request.headers.get('Content-Type')
#            if content_type == 'application/json':
#                body_json = request.get_json()
#                ign = ['city_id', 'user_id', 'created_at', 'updated_at', 'id']
#                for key, value in body_json.items():
#                    if key not in ign:
#                        setattr(found_place, key, value)
#                storage.save()
#                return jsonify(found_place.to_dict()), 200
#            else:
#                abort(400, 'Not a JSON')
#
#    elif request.method == 'DELETE':
#        key = 'Place.' + place_id
#        ids = [val.split('.')[1] for val in place_obj]
#        if place_id not in ids:
#            abort(404)
#        else:
#            storage.delete(place_obj[key])
#            storage.save()
#            return jsonify({}), 200
#
#    else:
#        abort(501)
