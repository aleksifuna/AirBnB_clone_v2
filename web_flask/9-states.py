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

cities = storage.all(City)
states = storage.all(State)


@app.route('/states', strict_slashes=False)
def state_list():
    """
    Displays a list of states in the db
    """
    return render_template('7-states_list.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def cities_list(id):
    """
    Displays a list of cities from a state in the db
    """
    return render_template(
            '9-states.html',
            cities=cities,
            states=states,
            id=id)


@app.teardown_appcontext
def teardown_db(exception=None):
    """
    removes the current session after each request
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
