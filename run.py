# coding: utf-8

"""
Create an application instance.
"""

from flask import request

from garagesale.app import create_app
from garagesale.settings import CONFIG

app = create_app(CONFIG)


@app.babel.localeselector
def get_locale():
    languages = CONFIG.LANGUAGES.keys()
    return request.accept_languages.best_match(languages)


if __name__ == "__main__":
    app.run()
