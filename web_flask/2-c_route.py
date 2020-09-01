#!/usr/bin/python3
"""Start a Flask web application"""

from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """/ route"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """/hbnb route"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def C_route(text):
    """/c/<text> route"""
    message = text.replace('_', ' ')
    return "C {}".format(message)


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
