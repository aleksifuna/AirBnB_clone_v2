#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models
from datetime import datetime
from models.city import City
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship(
            'City',
            backref='state',
            cascade='all, delete, delete-orphan'
            )


if getenv('HBNB_TYPE_STORAGE') == 'fs':
    @property
    def cities(self):
        '''returns a list of all cities from current state'''
        cities_list = []
        city_dict = models.storage.all(City)
        for key, value in city_dict.items():
            if value.state_id == self.id:
                cities_list.append(value)
        return cities_list
