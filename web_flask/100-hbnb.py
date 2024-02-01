#!/usr/bin/python3
"""
This module supplies a script that starts a flask web application
"""
from flask import Flask
from flask import render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.place import Place

app = Flask(__name__)

cities = storage.all(City)
states = storage.all(State)
amenities = storage.all(Amenity)
users = storage.all(User)
places = storage.all(Place)


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Displays states, cities and amenities for hbnb
    """
    return render_template(
            '100-hbnb.html',
            cities=cities,
            states=states,
            amenities=amenities,
            users=users,
            places=places
            )


@app.teardown_appcontext
def teardown_db(exception=None):
    """
    removes the current session after each request
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
