# -*- coding: utf-8 -*-

from flask.ext.script import Manager

from hairshopsearch import create_app, db

app = create_app()
manager = Manager(app)

@manager.command
def init_db():
    pass

@manager.command
def run():
    pass

manager.add_option('-c', '--config', dest='config',
        required=False, help='''Application config file to be used.\n
        Intended for local dev config.''')

if __name__ == '__main__':
    manager.run()
