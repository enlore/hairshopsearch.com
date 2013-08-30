# -*- encoding: utf-8 -*-
import os
from flask import Flask
from .frontend import frontend
from .user import user
from .extensions import db
from .salonmanager import salonmanager
from .stylist.views import stylist

BLUEPRINTS = [frontend, user, salonmanager, stylist]

def create_app(config=None, blueprints=None):
    """App factory, optionally passed a config file path from Manager"""
    if blueprints is None:
        blueprints = BLUEPRINTS
    app = Flask('hairshopsearch')
    configure_app(app, config)
    bootstrap_blueprints(app, blueprints)
    register_extensions(app)
    return app

def configure_app(app, config):
    app.config.from_object('hairshopsearch.config')
    if config is not None:
        app.logger.info(config)
        app.config.from_pyfile(config, silent=False)

def bootstrap_blueprints(app, blueprints):
    """Register blueprints on app."""
    for bp in blueprints:
        app.register_blueprint(bp)

def register_extensions(app):
    db.init_app(app)
