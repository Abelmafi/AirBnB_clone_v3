#!/usr/bin/python3
"""..."""

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


@app.route('/cities_by_states')
def cities_by_state():
    """..."""
    from models.state import State
    states = storage.all(State)
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def teardown(arg=None):
    storage.close()

if __name__ == '__main__':
    app.url_map.strict_slashes = False
    app.run(host='0.0.0.0', port=5000)
