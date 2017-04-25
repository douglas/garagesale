# coding: utf-8

import os
from envparse import env

# Try to read an env file with the development
# configs
env.read_envfile()


class Production(object):
    """ Production configuration """

    ENVIRONMENT = "production"
    SECRET_KEY = env("SECRET")
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    DEBUG = False
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/garagesale_prod"
    LANGUAGES = {
        "en": "English",
        "pt_br": "Brazilian Portuguese"
    }


class Development(Production):
    """ Development configuration """

    ENVIRONMENT = "development"
    DEBUG = True
    DEBUG_TB_ENABLED = True
    ASSETS_DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/garagesale_dev"


class Test(Production):
    """ Test configuration. """

    ENVIRONMENT = "test"
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/garagesale_test"

CONFIG = Development if env("FLASK_DEBUG") == "1" else Production
