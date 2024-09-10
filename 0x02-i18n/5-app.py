#!/usr/bin/env python3
"""Basic Babel setup for localization in a Flask application."""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _
from typing import Dict, Union

app = Flask(__name__)
babel = Babel(app)
app.url_map.strict_slashes = False


class Config:
    """Represents a Flask Babel configuration.

    Attributes:
        LANGUAGES (list): List of supported languages.
        BABEL_DEFAULT_LOCALE (str): Default locale.
        BABEL_DEFAULT_TIMEZONE (str): Default timezone.
    """
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
    """Retrieves a user based on a user id from request arguments.

    Returns:
        dict or None: A dictionary representing the user or None if not found.
    """
    user_id = request.args.get('login_as')
    if user_id:
        return users.get(int(user_id))
    return None


@app.before_request
def before_request() -> None:
    """Set the user in flask.g for the current request."""
    g.user = get_user()


@babel.localeselector
def get_locale() -> str:
    """Selects the best locale based on the following priority:

    1. Locale from URL parameters
    2. Locale from user settings
    3. Locale from request headers
    4. Default locale

    Returns:
        str: The locale code to be used for the current request.
    """
    locale = request.args.get('locale')
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
    """Render the index page based on user login status.

    Returns:
        str: The rendered HTML template.
    """
    if g.user:
        return render_template('5-index.html', username=g.user['name'])
    return render_template("5-index.html")


if __name__ == "__main__":
    app.run(debug=True)
