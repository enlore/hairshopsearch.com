from flask import Flask, Blueprint
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.security import Security
from flask_wtf import CsrfProtect
from .config import Config
from .core import db, ud, mail
import pkgutil
import importlib

def _create_app(pkg_name, pkg_path, config):
    """Internal app factory.
    """
    app = Flask(pkg_name)

    # a little jinja config - whitespace control
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.trim_blocks = True

    _config_app(app, config)
    _register_extensions(app)
    _bootstrap_blueprints(app, pkg_name, pkg_path)
    return app

def _config_app(app, config):
    app.config.from_object(Config)
    if config is not None:
        app.config.from_pyfile(config)

def _register_extensions(app):
    db.init_app(app)
    Security(app, ud)
    mail.init_app(app)
    toolbar = DebugToolbarExtension(app)
    CsrfProtect(app)

def _bootstrap_blueprints(app, pkg_name, pkg_path):
    """Sniff the blueprints out of the modules contained in the package's src
    tree and register them.

    Shoutout to @mattupstate, from whom I totally ganked this pattern.

    :param app: Flask instance
    :param pkg_name: Name of the package (__name__)
    :param pkg_path: Path where the package lives (__path__)
    """
    blueprints = []
    for _, name, _ in pkgutil.iter_modules(pkg_path):
        module = importlib.import_module('%s.%s' % (pkg_name, name))
        for item_name in dir(module):
            item = getattr(module, item_name)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)
            blueprints.append(item)
    return blueprints
