#!/usr/bin/python3
"""Start a Flask web application"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place


app = Flask(__name__)


@app.teardown_appcontext
def close(self):
    """Closes session"""
    storage.close()


@app.route('/hbnb', strict_slashes=False)
def hbnb_route():
    """/hbnb_filters route"""
    s = list(storage.all(State).values())
    c = list(storage.all(City).values())
    a = list(storage.all(Amenity).values())
    p = list(storage.all(Place).values())
    c.sort(key=lambda x: x.name)
    s.sort(key=lambda x: x.name)
    a.sort(key=lambda x: x.name)
    p.sort(key=lambda x: x.name)
    return render_template('100-hbnb.html\
', states=s, cities=c, amenities=a, places=p)


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
