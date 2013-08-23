# -*- encoding: utf-8 -*-
import os
from flask import Flask
from .frontend import frontend

BLUEPRINTS = [frontend]

def create_app(config=None, blueprints=None):
    """App factory, optionally passed a config file path from Manager"""
    if blueprints is None:
        blueprints = BLUEPRINTS
    app = Flask('hairshopsearch')
    configure_app(app, config)
    bootstrap_blueprints(app, blueprints)
    return app

def configure_app(app, config):
    """Use local production config or passed in dev config via Manager"""
    if config is None:
        config = os.path.join(app.root_path, 'production.cfg')

    app.config.from_pyfile(config)

def bootstrap_blueprints(app, blueprints):
    """Register blueprints on app."""
    for bp in blueprints:
        app.register_blueprint(bp)
