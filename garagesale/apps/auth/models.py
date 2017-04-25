# coding: utf-8

"""
Auth application models.
"""

import datetime as dt

from flask_login import UserMixin

from garagesale.extensions import bcrypt
from garagesale.database import CRUDModel
from garagesale.database import Column, String, Binary, DateTime, Boolean


class User(UserMixin, CRUDModel):
    """ An application user """

    __tablename__ = "users"
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(80), unique=True, nullable=False)
    _password_hash = Column(Binary(32), nullable=True)
    created_at = Column(DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(String(30), nullable=True)
    last_name = Column(String(30), nullable=True)
    active = Column(Boolean(), default=True)
    is_admin = Column(Boolean(), default=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, plaintext):
        self._password_hash = bcrypt.generate_password_hash(plaintext)

    def check_password(self, value):
        """ Check if the user password is correct """

        return bcrypt.check_password_hash(self._password_hash, value)

    @property
    def full_name(self):
        """ Full user name """

        return '{0} {1}'.format(self.first_name, self.last_name)

    def __repr__(self):
        if self.is_admin:
            return '<Admin {0}>'.format(self.username)

        return '<User {0}>'.format(self.username)
