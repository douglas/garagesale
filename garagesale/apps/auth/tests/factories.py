# coding: utf-8

"""
Factories to help in tests.
"""

from factory import Faker

from garagesale.tests.factories import BaseFactory
from garagesale.apps.auth.models import User


class UserFactory(BaseFactory):
    """ User factory """

    username = Faker("user_name")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = Faker("email")
    password = Faker("password")
    active = True

    class Meta:
        """Factory configuration."""

        model = User
