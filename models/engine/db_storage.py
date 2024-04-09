#!/usr/bin/python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base, BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


""" Define new class for engine database """

class DBStorage: 
    """ private attributes set to none """
    __engine = None
    __session = None

    def __init__(self):
        """Create the database engine and session"""
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        
        self.__engine = create_engine(f'mysql+mysqldb://{user}:{pwd}@{host}/{db}', pool_pre_ping=True)
        
        
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

        """ Miss all(self, cls=None)"""

    def all(self, cls=None):
        """Query all objects from the database"""
        classes = [User, State, City, Amenity, Place, Review]

        if cls:
            if isinstance(cls, str):
                cls = eval(cls)
            classes = [cls]
            
        objects = {}
        
        for cls in classes:
            for obj in self.__session.query(cls):
                key = '{}.{}'.format(type(obj).__name__, obj.id)
                objects[key] = obj
        return objects

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine, 
                                                         expire_on_commit=False))

    def close(self):
        """Close the current session"""  
        self.__session.remove()
