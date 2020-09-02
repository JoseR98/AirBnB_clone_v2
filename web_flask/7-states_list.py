#!/usr/bin/python3
"""Start a Flask web application"""

from flask import Flask, render_template
from models import storage
from models.state import State



app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """/states_list route"""
    states_list = list(storage.all(State).values())
    states_list.sort(key=lambda x: x.name)
    return render_template('7-states_list.html', states=states_list)

@app.teardown_appcontext
def close(self):
    """Closes session"""
    storage.close()

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
