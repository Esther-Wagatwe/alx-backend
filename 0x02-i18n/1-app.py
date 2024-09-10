#!/usr/bin/env python3
"""Basic Babel setup"""
from flask import Flask, render_template
from flask_babel import Babel


app = Flask(__name__)
babel = Babel(app)
app.url_map.strict_slasshes = False


class Config:
    """Represents a Flask Babel configuration."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@app.route('/')
def index():
    """default route"""
    return render_template("1-index.html",)


if __name__ == "__main__":
    app.run()
