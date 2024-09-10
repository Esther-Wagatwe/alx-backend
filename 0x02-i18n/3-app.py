#!/usr/bin/env python3
"""Basic Babel setup"""
from flask import Flask, render_template, request
from flask_babel import Babel


app = Flask(__name__)
babel = Babel(app)
app.url_map.strict_slashes = False


class Config:
    """Represents a Flask Babel configuration."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """
    Select the best match for the user's preferred language.
    Uses request.accept_languages to match against supported languages.
    """
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route('/')
def index():
    """default route"""
    return render_template("3-index.html",)


if __name__ == "__main__":
    app.run(debug=True)
