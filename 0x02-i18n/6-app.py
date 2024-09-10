#!/usr/bin/env python3
"""Basic Babel setup"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _
from typing import Dict, Union


app = Flask(__name__)
babel = Babel(app)
app.url_map.strict_slashes = False


class Config:
    """Represents a Flask Babel configuration."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Union[Dict, None]:
    """Retrieves a user based on a user id."""
    user_id = request.args.get('login_as')
    if user_id:
        return users.get(int(user_id))
    return None


@app.before_request
def before_request() -> None:
    """Set the user in flask.g."""
    g.user = get_user()


@babel.localeselector
def get_locale() -> str:
    """
    Select the best match for the user's preferred language.
    Follows the order of priority:
    1. Locale from URL parameters
    2. Locale from user settings
    3. Locale from request headers
    4. Default locale
    """
    locale = request.args.get('locale', None)
    if locale and locale in app.config['LANGUAGES']:
        return locale
    if g.user and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user['locale']
    locale = request.accept_languages.best_match(app.config['LANGUAGES'])
    if locale:
        return locale
    return app.config['BABEL_DEFAULT_LOCALE']


@app.route('/')
def index() -> str:
    """default route"""
    if g.user:
        return render_template('5-index.html', username=g.user['name'])
    return render_template("5-index.html",)


# app.before_request(before_request)

if __name__ == "__main__":
    app.run(debug=True)
