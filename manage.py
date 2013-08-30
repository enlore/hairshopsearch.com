# -*- coding: utf-8 -*-

from flask.ext.script import Manager, Server, Command
from hairshopsearch import create_app
from hairshopsearch.extensions import db

manager = Manager(create_app())

class Init_db(Command):
    """Initializes a fresh db"""
    def run(self):
        manager.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/hairshopsearch.db'
        manager.app.config['SQLALCHEMY_ECHO'] = True
        db.drop_all(app=manager.app)
        db.create_all(app=manager.app)

manager.add_command('init_db', Init_db())
manager.add_command('run', Server(host='127.0.0.1',port=9007))
manager.add_option(
        '-c', '--config', dest='config',
        required=False, 
        help="""Application config file to be used. Intended for local dev \
                config."""
        )

if __name__ == '__main__':
    manager.run()
