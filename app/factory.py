from flask import Flask
from config import Config

def create_app(config=None):
    app = Flask('hairshopsearch')
    config_app(app, config)
    return app

def config_app(app, config):
    app.config.from_object(Config)
    if config is not None:
        app.config.from_pyfile(config)
