#!/usr/bin/python3
"""
This module supplies a script that starts a flask web application
"""
from flask import Flask
from flask import render_template
from markupsafe import escape
from models import storage
from models.state import State
from models.city import City
app = Flask(__name__)

states = storage.all(State)
cities = storage.all(City)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """
    Displays a list of cities by state in the db
    """
    return render_template('8-cities_by_states.html',
            states=states,
            cities=cities)


@app.teardown_appcontext
def teardown_db(exeption):
    """
    removes the current session after each request
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
