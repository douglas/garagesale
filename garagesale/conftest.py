# coding: utf-8

"""
Defines pytest fixtures that will be used in other tests.
"""

import pytest
from webtest import TestApp

from garagesale.app import create_app
from garagesale.settings import Test
from garagesale.database import db as _db
from garagesale.apps.auth.tests.factories import UserFactory


@pytest.fixture
def app():
    """An application for the tests."""
    _app = create_app(Test, initial_admin=False)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture
def testapp(app):
    """A Webtest app."""
    return TestApp(app)


@pytest.yield_fixture(scope='function')
def db(app):
    """ A database for the tests. """
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


@pytest.fixture
def user(db):
    """ A user for the tests """

    user = UserFactory(username="testuser", password="testpass")
    db.session.commit()
    return user
