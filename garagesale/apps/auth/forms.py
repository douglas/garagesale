# coding: utf-8

"""
Auth application forms
"""

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired
from flask_babel import gettext as _

from .models import User


class LoginForm(FlaskForm):
    """ Login form """

    username = StringField(_("Username"), validators=[DataRequired()])
    password = PasswordField(_("New Password"), [DataRequired()])
    submit = SubmitField(_("Submit"))

    def __init__(self, *args, **kwargs):
        """ """

        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """ Validate the login form """

        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            self.username.errors.append(_("Please inform the username and password"))
            return False

        # Lets check if the user is valid
        self.user = User.query.filter_by(username=self.username.data).first()

        if self.user is None:
            self.username.errors.append(_("Invalid username or password"))
            return False
        else:
            if self.user.check_password(self.password.data) is False:
                self.username.errors.append(_("Invalid username or password"))
                return False

            if self.user.active is False:
                self.username.errors.append(_("User not activated"))
                return False

        return True
