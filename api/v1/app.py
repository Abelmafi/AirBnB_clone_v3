#!/usr/bin/python3
"""Api creations"""


from flask import Flask
from models.storage import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext()
def teardown():
    """..."""
    storage.close()


if __name__ == '__main__':
    """..."""
    app.run(host=get.env('HBNB_API_HOST'),
            port=get.env('HBNB_API_PORT'),
            threaded=True)
