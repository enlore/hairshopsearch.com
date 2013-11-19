#!/home/no/.venvs/hairshopsearch/bin/python
from flask.ext.script import Manager, Server, Shell
from app import create_app
from app.core import db, ud
from app.models import (User, Role, Provider, Address, Photo, Review,
                                Consumer, Menu, Gallery, Location)
from app.helpers import JSONEncoder, acceptable_url_string
from app.indexer import indexer
from app.config import Config
from pprint import pprint

import csv

m = Manager(create_app)

@m.command
def reset_db():
    db.drop_all()
    db.create_all()

@m.command
def create_index():
    indexer.create_index('provider')

def _consume_csv(filename):
    entities = []
    first = True
    with open(filename, 'r') as f:
        for row in csv.reader(f):
            if first:
                keys = row
                first = False
            else:
                entity = dict()
                for key, col in zip(keys, row):
                    entity[key] = col
                entities.append(entity)
        for entity in entities:
            lat_string = entity['lat'].strip()
            lon_string = entity['lon'].strip()
            if '\xc2\xb0' in lat_string:
                deg, min = lat_string.split('\xc2\xb0')
                # bleah
                entity['lat'] = float(deg) + float(min[0:-1])/60

            if '\xc2\xb0' in lon_string:
                deg, min = lon_string.split('\xc2\xb0')
                # bleah
                entity['lon'] = float(deg) + float(min[0:-1])/60
    return entities

@m.command
def mock_from_csv(filename):
     entities = _consume_csv(filename)
     for entity in entities:
         p = Provider(business_name=entity.pop('business_name'))
         p.location = Location(lat=entity.pop('lat'), lon=entity.pop('lon'))
         p.address = Address(**entity)
         p.business_url = acceptable_url_string(p.business_name,
                 Config.ACCEPTABLE_URL_CHARS)
         db.session.add(p)
         db.session.commit()


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
