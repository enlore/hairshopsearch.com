#!/home/no/.venvs/hairshopsearch/bin/python
from flask.ext.script import Manager, Server, Shell
from app import create_app
from app.core import db, ud
from app.user.models import (User, Role, Provider, Address, Photo, Review,
                                Consumer, Menu, Gallery)
from app.helpers import JSONEncoder
from tests.data import mockup_data
from pprint import pprint

m = Manager(create_app)

@m.command
def reset_db():
    db.drop_all()
    db.create_all()
    mockup_data()

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
           Photo=Photo,
           Menu=Menu,
           p=Provider.query.get(4),
           c=Consumer.query.first(),
           jsoner=JSONEncoder(),
           pprint=pprint
            )

m.add_option('-c', '--config', dest='config', required=False)
m.add_command('run', Server(port='9016'))
m.add_command('shell', Shell(make_context=_make_context))


if __name__ == '__main__':
    m.run()
