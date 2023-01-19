#!/usr/bin/python3
"""..."""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """..."""
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def stats():
    """..."""
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User

    cls_name = {"amenities": Amenity, "cities": City,
                "places": Place, "reviews": Review,
                "states": State, "users": User}
    json_dict = {}
    for name, cls in cls_name.items():
        json_dict[name] = storage.count(cls)

    return jsonify(json_dict)
