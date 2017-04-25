# coding: utf-8

from flask_sqlalchemy import SQLAlchemy
from past.builtins import basestring

db = SQLAlchemy()

# Aliases to some SQLAlchemy definitions
Column = db.Column
Model = db.Model
String = db.String
Binary = db.Binary
DateTime = db.DateTime
Boolean = db.Boolean
Integer = db.Integer


# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK(object):
    """
    Base class which provides automated table name
    and surrogate primary key column.
    """

    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """ Get record by ID. """

        if any((isinstance(record_id, basestring) and record_id.isdigit(),
                isinstance(record_id, (int, float)))):
            return cls.query.get(int(record_id))


class CRUDMixin(object):
    """
    Mixin that adds convenience methods for
    CRUD (create, read, update, delete) operations.
    """

    @classmethod
    def create(cls, **kwargs):
        """ Create a new record and save it the database """

        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """ Update specific fields of a record """

        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """ Save the record """

        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """ Remove the record from the database. """

        db.session.delete(self)
        return commit and db.session.commit()


class CRUDModel(SurrogatePK, CRUDMixin, db.Model):
    """ Base model class that includes CRUD convenience methods. """

    __abstract__ = True
