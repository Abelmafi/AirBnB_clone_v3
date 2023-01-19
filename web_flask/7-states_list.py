#!/usr/bin/python3
"""This script starts a Flask web application"""


from flask import Flask
from models import storage
from flask import render_template
app = Flask(__name__)


@app.route('/states_list')
def state_list():
    """..."""
    from models.state import State
    states = storage.all(State)
    sorted_states = sorted(states.values(), key=lambda state: state.name)
    return render_template('7-states_list.html', sorted_states=sorted_states)


@app.teardown_appcontext
def teardown(arg=None):
    storage.close()

if __name__ == '__main__':
    app.url_map.strict_slashes = False
    app.run(host='0.0.0.0', port=5000)
