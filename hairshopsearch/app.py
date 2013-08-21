# -*- encoding: utf-8 -*-
import os
from flask import Flask
from .config import ProConfig

def create_app(config=None):
    """App factory, optionally passed a config file path from Manager"""
    app = Flask('hairshopsearch')
    configure_app(app, config)
    bootstrap_blueprints(app)
    return app

def configure_app(app, config):
    """Use local production config or passed in dev config via Manager"""
    if config is None:
        config = os.path.join(app.root_path, 'production.cfg')

    app.config.from_pyfile(config)

def bootstrap_blueprints(app):
    """Register blueprints on app."""
    for bp in app.config['BLUEPRINTS']:
        app.register_blueprint(bp)
