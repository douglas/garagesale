# coding: utf-8

"""
User Model unit tests.
"""

import datetime as dt

import pytest

from garagesale.apps.auth.models import User
from .factories import UserFactory


@pytest.mark.usefixtures("db")
class TestUser:
    """ Tests the User model """

    def test_get_by_id_unexistent_user(self):
        """ Try to get an unexistent user by ID """

        retrieved = User.get_by_id(9999)
        assert retrieved is None

    def test_created_at_defaults_to_datetime(self):
        """ Test creation date """

        user = User(username="foo", email="foo@bar.com")
        user.save()
        assert bool(user.created_at)
        assert isinstance(user.created_at, dt.datetime)

    def test_cant_access_password(self):
        """ Test that we cannot access the password directly """

        user = User(username="foo", email="foo@bar.com")
        user.save()

        with pytest.raises(AttributeError) as excinfo:
            print(user.password)
        assert excinfo.typename == "AttributeError"

    def test_factory(self, db):
        """ Test user factory """

        user = UserFactory(password="myprecious")
        db.session.commit()

        assert bool(user.username)
        assert bool(user.email)
        assert bool(user.created_at)
        assert user.is_admin is False
        assert user.active is True
        assert user.check_password("myprecious")

    def test_check_password(self):
        """ Check password """

        user = User.create(
            username="foo",
            email="foo@bar.com",
            password="foobarbaz123"
        )
        assert user.check_password("foobarbaz123") is True
        assert user.check_password("barfoobaz") is False

    def test_delete_user(self):
        """ Delete user """

        user = User.create(
            username="foo",
            email="foo@bar.com",
            password="foobarbaz123"
        )
        user.save()

        user_id = user.id
        retrieved = User.get_by_id(user_id)
        assert retrieved == user

        # Delete the user
        user.delete()
        retrieved = User.get_by_id(user_id)
        assert retrieved is None

    def test_update_user(self):
        """ Update user """

        user = User.create(
            username="foo",
            email="foo@bar.com",
            password="foobarbaz123"
        )
        user.save()

        # Update user information
        user.update(email="test@test.com")
        user.update(first_name="Test")

        # Update user information in batch
        user.last_name = "User"
        user.active = False
        user.is_admin = True
        user.save()

        # Test if it was really updated
        assert user.email == "test@test.com"
        assert user.first_name == "Test"
        assert user.last_name == "User"
        assert user.active is False
        assert user.is_admin is True

    def test_full_name(self):
        """ User full name """

        user = UserFactory(first_name="Foo", last_name="Bar")
        assert user.full_name == "Foo Bar"
