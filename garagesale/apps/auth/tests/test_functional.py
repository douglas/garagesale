# coding: utf-8

"""
Functional tests for the user app - Login
"""

import pytest

from flask_babel import gettext as _


def test_login_returns_200(testapp):
    """ Login page """

    client = testapp.get('/login')
    assert client.status_code == 200


def test_login_without_required_data(testapp):
    """
    Tests that a user can't log in without
    filling the required data
    """

    res = testapp.get('/login')

    form = res.forms["login_form"]
    form['username'] = ""
    form['password'] = ""

    res = form.submit()

    assert _("Please inform the username and password") in res


@pytest.mark.usefixtures("user")
def test_login_successful_show_message(testapp):
    """ Tests if there is a success message when an user logs in """

    res = testapp.get('/login')

    form = res.forms["login_form"]
    form['username'] = "testuser"
    form['password'] = "testpass"

    res = form.submit().follow()
    assert _("You are logged in.") in res


@pytest.mark.usefixtures("user")
def test_invalid_login_show_message(testapp):
    """
    Tests if there is an unsuccessful message when
    there is login error
    """

    res = testapp.get('/login')
    form = res.forms["login_form"]
    form['username'] = "wronguser"
    form['password'] = "wrongpass"

    res = form.submit()
    assert _("Invalid username or password") in res


@pytest.mark.usefixtures("user")
def test_invalid_password_show_message(testapp):
    """
    Tests if an user tries to log in with
    an invalid password
    """

    res = testapp.get('/login')
    form = res.forms["login_form"]
    form['username'] = "testuser"
    form['password'] = "wrongpass"

    res = form.submit()
    assert _("Invalid username or password") in res


def test_inactive_user_show_message(user, testapp):
    """
    Tests if an inactive user tries to log in
    """

    user.update(active=False)

    res = testapp.get('/login')
    form = res.forms["login_form"]
    form['username'] = "testuser"
    form['password'] = "testpass"

    res = form.submit()
    assert _("User not activated") in res
