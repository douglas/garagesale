# coding: utf-8

"""
Extensions module.
Each extension is initialized in the app factory located in app.py.
"""
from flask_babel import gettext as _
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = _("Please log in to access this page.")
bootstrap = Bootstrap()
migrate = Migrate()
