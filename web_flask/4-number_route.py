#!/usr/bin/python3
"""
This module supplies a script that starts a flask web application
"""
from flask import Flask
from markupsafe import escape
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """
    Displays Hello HBNB!
    """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Displays HBNB
    """
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def ctext(text):
    """
    Displays C followed by text that is passed
    """
    return f'C {escape(text)}'.replace('_', ' ')


@app.route('/python/<text>', strict_slashes=False)
@app.route('/python/', defaults={'text': 'is_cool'}, strict_slashes=False)
def pythontext(text):
    """
    Displays python followed by text that is passed
    """
    return f'Python {escape(text)}'.replace('_', ' ')


@app.route('/number/<int:n>', strict_slashes=False)
def numberint(n):
    """
    Displays n is a number only if n is an integer
    """
    return f'{n} is a number'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
