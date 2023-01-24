#!/usr/bin/python3
"""..."""


from api.v1.views import app_views
from models.base_model import BaseModel
from flask import Flask, jsonify, abort, request


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def users(user_id=None):

    return "hi there"
