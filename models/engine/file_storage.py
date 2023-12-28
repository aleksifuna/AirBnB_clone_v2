#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}
    classes = {
                'BaseModel': BaseModel, 'User': User, 'Place': Place,
                'State': State, 'City': City, 'Amenity': Amenity,
                'Review': Review
            }

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls:
            temp = {}

            # if the cls parameter is passed in the correct class type
            target_class = cls

            # check if the cls parameter is passed in as string
            if type(cls) == str:
                target_class = FileStorage.classes[cls]

            for key, value in FileStorage.__objects.items():
                if isinstance(value, target_class):
                    temp[key] = value
            return temp
        else:
            return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""

        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = FileStorage.classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        delete obj from __objects if it’s inside - if obj is equal to None
        the method should not do anything
        """

        if obj:
            my_key = None
            for key, value in FileStorage.__objects.items():
                if obj == value:
                    my_key = key

            if my_key:
                FileStorage.__objects.pop(my_key)
        else:
            pass

    @property
    def cities(self):
        """getter function for City instances"""
        obj = session.query(City).join(State, City.state_id == State.id)
        return (obj)

    @property
    def reviews(self):
        """getter function for Review instances"""
        obj = session.query(Review).join(Place, Review.place_id == Place.id)
        return (obj)
