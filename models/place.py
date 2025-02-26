#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Table
from os import getenv

if getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table(
            'place_amenity',
            Base.metadata,
            Column(
                'place_id',
                String(60),
                ForeignKey('places.id'),
                primary_key=True,
                nullable=False
                ),
            Column(
                'amenity_id',
                String(60),
                ForeignKey('amenities.id'),
                primary_key=True,
                nullable=False)
            )


class Place(BaseModel, Base):
    ''' A place to stay '''
    __tablename__ = 'places'

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)

        reviews = relationship(
                'Review',
                backref='place',
                cascade='all, delete, delete-orphan'
                )
        amenities = relationship(
                'Amenity',
                secondary=place_amenity,
                viewonly=False,
                backref='place_amenities'
                )
    else:
        city_id = ''
        user_id = ''
        name = ''
        description = ''
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            ''' returns a list of review instances with place_id = self.id'''
            from models import storage
            all_reviews = storage.all(Review)
            reviews_list = []
            for review in all_reviews.values():
                if review.id == self.id:
                    reviews_list.append(review)
            return reviews_list

        @property
        def amenities(self):
            ''' returns a list of amenity instances with id in amenity_ids'''
            from models import storage
            all_amenities = storage.all(Amenity)
            amenities_list = []
            for amenity in all_amenities:
                if amenity.id in self.amenity_ids:
                    amenities_list.append(amenity)
            return amenities_list

        @amenities.setter
        def amenities(self, obj):
            ''' adds amenity.id to amenity_ids list '''
            if obj is not None:
                if isinstance(obj, Amenity):
                    if obj.id not in self.amenity_ids:
                        self.amenity_ids.append(obj.id)
