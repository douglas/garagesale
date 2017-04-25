# coding: utf-8

"""
The app module, containing the app factory function.
"""

from flask import Flask
from flask_babel import Babel

from garagesale import commands
from garagesale.apps import public, auth
from garagesale.settings import CONFIG, Production
from garagesale.extensions import bcrypt, login_manager, bootstrap, migrate
from garagesale.database import db


def create_app(environment=Production, initial_admin=True):
    """
    The application factory
    """

    app = Flask(__name__.split(".")[0])
    app.babel = Babel(app)
    app.config.from_object(environment)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)

    if initial_admin is True:
        create_admin(app)

    return app


def create_admin(app):
    """ Add the admin user """

    from garagesale.apps.auth.models import User

    with app.app_context():
        if User.query.count() == 0:
            admin = User.create(
                username="admin",
                email="admin@admin.com",
                password="admin",
                active=True,
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("Initial admin user added.")


def register_extensions(app):
    """ Register Flask extensions. """

    bcrypt.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    if CONFIG.ENVIRONMENT == "development":
        from flask_debugtoolbar import DebugToolbarExtension
        debug_toolbar = DebugToolbarExtension()
        debug_toolbar.init_app(app)


def register_blueprints(app):
    """ Register Flask blueprints. """

    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(auth.views.blueprint)


def register_commands(app):
    """ Register Click commands """

    app.cli.add_command(commands.test)
    app.cli.add_command(commands.clean)
