from flask import Flask, Blueprint
from config import Config
import pkgutil
import importlib

def _create_app(pkg_name, pkg_path, config):
    """Internal app factory.
    """
    app = Flask(pkg_name)
    _config_app(app, config)
    _bootstrap_blueprints(app, pkg_name, pkg_path)
    return app

def _config_app(app, config):
    app.config.from_object(Config)
    if config is not None:
        app.config.from_pyfile(config)

def _bootstrap_blueprints(app, pkg_name, pkg_path):
    blueprints = []
    for _, name, _ in pkgutil.iter_modules(pkg_path):
        module = importlib.import_module('%s.%s' % (pkg_name, name))
        for item_name in dir(module):
            item = getattr(module, item_name)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)
            blueprints.append(item)
    return blueprints
