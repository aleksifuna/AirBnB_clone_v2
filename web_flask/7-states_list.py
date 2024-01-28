#!/usr/bin/python3
"""
This module supplies a script that starts a flask web application
"""
from flask import Flask
from flask import render_template
from markupsafe import escape
from models import storage
from models.state import State
app = Flask(__name__)

states = storage.all(State)
objs = sorted(states.items(), key=lambda x: x[1].name)


@app.route('/states_list', strict_slashes=False)
def state_list():
    """
    Displays a list of states in the db
    """
    return render_template('7-states_list.html', objs=objs)


@app.teardown_appcontext
def teardown_db(exeption):
    """
    removes the current session after each request
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
