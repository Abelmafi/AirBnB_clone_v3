#!/usr/bin/python3
"""Define storage engine using MySQL database
"""
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker, Session
from os import getenv

all_classes = {'State': State, 'City': City,
               'User': User, 'Place': Place,
               'Review': Review, 'Amenity': Amenity}


class DBStorage:
    """This class manages MySQL storage using SQLAlchemy

    Attributes:
        __engine: engine object
        __session: session object
    """
    __engine = None
    __session = None

    def __init__(self):
        """Create SQLAlchemy engine
        """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'.
                                      format(getenv('HBNB_MYSQL_USER'),
                                             getenv('HBNB_MYSQL_PWD'),
                                             getenv('HBNB_MYSQL_HOST'),
                                             getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Return: dictionary (<class-name>.<object-id>: <obj>)"""
        obj_dict = {}

        if cls:
            for row in self.__session.query(cls).all():
                obj_dict.update({'{}.{}'.
                                format(type(cls).__name__, row.id,): row})
        else:
            for key, val in all_classes.items():
                for row in self.__session.query(val):
                    obj_dict.update({'{}.{}'.
                                    format(type(row).__name__, row.id,): row})
        return obj_dict

    def new(self, obj):
        """Add object to current database session"""

        self.__session.add(obj)

    def save(self):
        """Commit current database session"""

        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from database session
        """
        if obj:
            c_name = all_classes[type(obj).__name__]

            self.__session.query(c_name).filter(c_name.id == obj.id).delete()

    def reload(self):
        """Create database session
        """
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine,
                               expire_on_commit=False)
        self.__session = scoped_session(session)

    def close(self):
        """Close scoped session
        """
        self.__session.remove()
