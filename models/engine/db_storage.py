#!/usr/bin/python3
"""
responsible for storing our models to the database
"""
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from sqlalchemy import create_engine
from os import getenv
import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """
    defines the dbstorage class methods and attributes
    """
    __engine = None
    __session = None
    username = getenv('HBNB_MYSQL_USER')
    password = getenv('HBNB_MYSQL_PWD')
    db_name = getenv('HBNB_MYSQL_DB')
    host = getenv('HBNB_MYSQL_HOST')

    def __init__(self):
        """ Initializes the instance"""

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            DBStorage.username, DBStorage.password, DBStorage.host,
            DBStorage.db_name
                ), pool_pre_ping=True)
        if getenv('HBNB_ENV') == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """returns a dictionary
        Return:
            returns a dictionary of __object
        """
        dic = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for obj in query:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                dic[key] = obj
        else:
            obj_list = [State, City, User, Place, Review, Amenity]
            for clss in obj_list:
                query = self.__session.query(clss)
                for obj in query:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    dic[key] = obj
        return (dic)

    def new(self, obj):
        """adds the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commits all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes from current database session obj is not none"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """reload data from the databases"""
        Base.metadata.create_all(self.__engine)
        ses_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(ses_factory)
        self.__session = Session

    def close(self):
        """ calls remove() method on __session"""
        self.__session.remove()
