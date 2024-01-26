#!/usr/bin/python3
"""
This module supplies a script that starts a flask web application
"""
from flask import Flask
from flask import render_template
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


@app.route('/number_template/<int:n>', strict_slashes=False)
def numbertemplateint(n):
    """
    Displays n is a number only if n is an integer
    """
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def oddeven(n):
    """
    Displays n is a number only if n is an integer and if odd or even
    """
    return render_template('6-number_odd_or_even.html', n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
