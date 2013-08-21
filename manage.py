# -*- coding: utf-8 -*-

from flask.ext.script import Manager, Server
from flask import Flask
#from hairshopsearch import create_app, db

#app = create_app()
app = Flask('hairshopsearch')
manager = Manager(app)

@manager.command
def init_db():
    """Initializes a fresh db"""
    print 'Initdbing!'

manager.add_command('run', Server(host='127.0.0.1',port=9007))
manager.add_option(
        '-c', '--config', dest='config',
        required=False, 
        help='''Application config file to be used. Intended for local dev config.'''
        )

if __name__ == '__main__':
    manager.run()
