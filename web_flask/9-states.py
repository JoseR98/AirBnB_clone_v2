#!/usr/bin/python3
"""Start a Flask web application"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City


app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states():
    """/states_list route"""
    states_list = list(storage.all(State).values())
    states_list.sort(key=lambda x: x.name)
    return render_template('9-states.html', states=states_list)


@app.route('/states/<id>', strict_slashes=False)
def state_cities_list(id=None):
    """/cities_by_states route"""
    e = None
    states = storage.all(State)
    c = list(storage.all(City).values())
    c.sort(key=lambda x: x.name)
    if id:
        key = "State." + id
        if key in states.keys():
            e = states[key]
    return render_template('9-states.html', cities=c, state=e, id=id)


@app.teardown_appcontext
def close(self):
    """Closes session"""
    storage.close()

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
