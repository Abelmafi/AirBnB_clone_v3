#!/usr/bin/python
""" holds class Place"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

if models.storage_t == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True))


class Place(BaseModel, Base):
    """Representation of Place """
    if models.storage_t == 'db':
        __tablename__ = 'places'
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
        reviews = relationship("Review", backref="place")
        amenities = relationship("Amenity", secondary="place_amenity",
                                 backref="place_amenities",
                                 viewonly=False)
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    def __init__(self, *args, **kwargs):
        """initializes Place"""
        super().__init__(*args, **kwargs)

    if models.storage_t != 'db':
        @property
        def reviews(self):
            """getter attribute returns the list of Review instances"""
            from models.review import Review
            review_list = []
            all_reviews = models.storage.all(Review)
            for review in all_reviews.values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """getter attribute returns the list of Amenity instances"""
            from models.amenity import Amenity
            amenity_list = []
            all_amenities = models.storage.all(Amenity)
            for amenity in all_amenities.values():
                if amenity.place_id == self.id:
                    amenity_list.append(amenity)
            return amenity_list
#"""This is the place class"""
#import models
#from models.base_model import BaseModel, Base
#from sqlalchemy import Column, String, Float, Integer, ForeignKey, Table
#from sqlalchemy.orm import relationship
#from os import getenv
#
#
#place_amenity = Table('place_amenity', Base.metadata,
#                      Column('place_id', String(60),
#                             ForeignKey('places.id', onupdate='CASCADE',
#                                        ondelete='CASCADE'),
#                             primary_key=True, nullable=False),
#                      Column('amenity_id', String(60),
#                             ForeignKey('amenities.id', onupdate='CASCADE',
#                                        ondelete='CASCADE'),
#                             primary_key=True, nullable=False))
#
#
#class Place(BaseModel, Base):
#    """This is the class for Place"""
#    __tablename__ = 'places'
#
#    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
#    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
#    name = Column(String(128), nullable=False)
#    description = Column(String(1024), nullable=True)
#    number_rooms = Column(Integer, nullable=False, default=0)
#    number_bathrooms = Column(Integer, nullable=False, default=0)
#    max_guest = Column(Integer, nullable=False, default=0)
#    price_by_night = Column(Integer, nullable=False, default=0)
#    latitude = Column(Float, nullable=True)
#    longitude = Column(Float, nullable=True)
#    amenity_ids = []
#
#    if models.storage_t == 'db':
#        reviews = relationship('Review', backref='place')
#        amenities = relationship('Amenity', backref='place_amenities',
#                                 secondary='place_amenity',
#                                 viewonly=False)
#
#    else:
#        @property
#        def reviews(self):
#            """ getter returns list of reviews """
#            list_of_reviews = []
#            all_reviews = models.strage.all(Review)
#            for review in all_reviews.values():
#                if review.place_id == self.id:
#                    list_of_reviews.append(review)
#            return list_of_reviews
#
#        @property
#        def amenities(self):
#            """ getter returns list of amenities """
#            list_of_amenities = []
#            all_amenities = models.storage.all(Amenity)
#            for key, obj in all_amenities.items():
#                if key in self.amentiy_ids:
#                    list_of_amenities.append(obj)
#            return list_of_amenities
#
#        @amenities.setter
#        def amenities(self, obj=None):
#            """Set amenity_ids"""
#            if type(obj).__name__ == 'Amenity':
#                new_amenity = 'Amenity' + '.' + obj.id
#                self.amenity_ids.append(new_amenity)
