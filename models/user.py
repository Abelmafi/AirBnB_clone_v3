#!/usr/bin/python3
"""This is the user class"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """This is the class for user
    Attributes:
        email: email address
        password: password for you login
        first_name: first name
        last_name: last name
    """
    if models.storage_t == 'db':
        __tablename__ = 'users'

        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)

        reviews = relationship('Review', cascade='all, delete', backref='user')
        places = relationship('Place', cascade='all, delete', backref='user')
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
        if self.password:
            hashed_password = hashlib.md5(self.password.encode("utf-8"))
            self.password = hashed_password.hexdigest()
