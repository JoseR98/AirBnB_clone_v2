#!/usr/bin/python3
"""This module defines a Database class to manage file storage"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from models.base_model import Base
from models.state import State
from models.city import City


class DBStorage:
    """ """
    __engine = None
    __session = None

    def __init__(self):
        """ """
        user = os.getenv('HBNB_MYSQL_USER')
        pswd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}\
'.format(user, pswd, host, db), pool_pre_ping=True)
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ """
        instances = {}
        if cls:
            records = self.__session.query(cls).all()
            for row in records:
                key = cls.__name__ + '.' + row.id
                instances[key] = row
        else:
            clases = [State, City]
            for clase in clases:
                records = self.__session.query(clase).all()

                for record in records:
                    key = "{}.{}".format(type(record).__name__, record.id)
                    instances[key] = record
        return instances

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()
    
    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)
    
    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_factory  = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()