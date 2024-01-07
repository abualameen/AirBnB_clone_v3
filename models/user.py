#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """Initializes user"""
        super().__init__(*args, **kwargs)
        # Check if 'password' exists in kwargs and if it does, hash it
        if 'password' in kwargs:
            self.password = kwargs['password']

    @property
    def password(self):
        """Getter for password."""
        return self.__password

    @password.setter
    def password(self, value):
        """Setter for password, hashing it using MD5."""
        self.__password = hashlib.md5(value.encode()).hexdigest()
