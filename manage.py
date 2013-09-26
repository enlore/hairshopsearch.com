#!/home/no/.venvs/hairshopsearch/bin/python
from flask.ext.script import Manager, Server, Shell 
from app import create_app
from app.core import db, ud
from app.user.models import (User, Role, Provider, Address, Photo, Review,
                                Gallery)

m = Manager(create_app)

def _make_context():
    return dict(
           app=create_app(),
           db=db,
           ud=ud,
           User=User,
           Role=Role,
           Provider=Provider,
           Review=Review,  
           Address=Address, 
           Gallery=Gallery,
           Photo=Photo
            )

m.add_command('run', Server(port='9016'))
m.add_command('shell', Shell(make_context=_make_context))

if __name__ == '__main__':
    m.run()
