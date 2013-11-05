from flask import Flask, Blueprint, render_template
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.security import Security
from flask_wtf import CsrfProtect
from .config import Config
from .core import db, sec, mail, HSSError
from .helpers import ellipsize
from .search.forms import SearchForm
import pkgutil
import importlib
import locale
from logging import Formatter, ERROR, INFO
from logging.handlers import RotatingFileHandler, SMTPHandler

locale.setlocale(locale.LC_ALL, '')

def pretty_cash(amount):
    return locale.currency(amount)

def _create_app(pkg_name, pkg_path, config):
    """Internal app factory.
    """
    app = Flask(pkg_name)

    # a little jinja config - whitespace control
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.trim_blocks = True

    app.jinja_env.filters['cash'] = pretty_cash
    app.jinja_env.filters['ellipsize'] = ellipsize

    app.jinja_env.globals['search_form'] = SearchForm

    @app.errorhandler(HSSError)
    def handle_internal_error(error):
        raise error

    @app.errorhandler(404)
    def four_oh_four(msg):
        return render_template('errors/404.html')

    _config_app(app, config)
    _register_extensions(app)
    _bootstrap_blueprints(app, pkg_name, pkg_path)
    _leverage_logging(app)
    return app

def _config_app(app, config):
    app.config.from_object(Config)
    if config is not None:
        app.config.from_pyfile(config, silent=True)

def _register_extensions(app):
    db.init_app(app)
    sec.init_app(app)
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

def _leverage_logging(app):
    if app.config['FILE_LOGGING']:
        rfh = RotatingFileHandler(app.config['FILE_LOG'])
        rfh.setLevel(INFO)
        rfh.setFormatter(Formatter("""
    [%(pathname)s]
    %(asctime)s
    %(levelname)s in %(module)s.%(funcName)s, line %(lineno)d:
        %(message)s"""))
        app.logger.addHandler(rfh)

    if app.config['MAIL_LOGGING']:
        smtph = SMTPHandler(
                (app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                app.config['MAIL_LOG_FROM'],
                app.config['MAIL_LOG_ADMINS'],
                '[[ Houston, we have a problem ]]',
                (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']),
                () # lol empty tuple for secure kwarg
                )
        smtph.setLevel(ERROR)
        smtph.setFormatter(Formatter("""
    IT BARFED (the app, I mean)
        Level: %(levelname)s
        Path: %(pathname)s
        Function: %(module)s.(%funcName)s at %(lineno)d
        Time: %(asctime)s
        Message:
            %(message)s

        """))
        app.logger.addHandler(smtph)

