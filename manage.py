#!/home/no/.venvs/hairshopsearch/bin/python
from flask.ext.script import Manager, Server, Shell
from flask_security.utils import encrypt_password
from app import create_app
from app.core import db, ud
from app.models import (User, Role, Photo, Gallery)
from app.provider.models import Provider, Address, Menu, MenuItem, Location
from app.consumer.models import Consumer
from app.models import Gallery, Photo
from app.helpers import JSONEncoder, acceptable_url_string
from app.indexer import indexer
from app.config import Config
from pprint import pprint

import csv
import random
import datetime

m = Manager(create_app)

@m.command
def reset_db():
    db.drop_all()
    db.create_all()

    # Provider
    password = encrypt_password('password')
    p = Provider(user=ud.create_user(email="n.e.lorenson@gmail.com", password=password),
            business_name = 'Sparky\'s',
            business_url = 'sparkys'
            )
    p.user.confirmed_at = datetime.date.today()

    p.menus.append(Menu(menu_type="barber"))
    p.menus[0].menu_items.append(MenuItem(name="Haircut", price="25", description="We cut your hair"))
    p.menus[0].menu_items.append(MenuItem(name="Line out", price="10", description="A quick line out"))
    p.menus[0].menu_items.append(MenuItem(name="Shave", price="14", description="Shave your face"))

    p.menus.append(Menu(menu_type="salon"))
    p.menus[1].menu_items.append(MenuItem(name="Color", price="40", description="A lovely color for your hair"))
    p.menus[1].menu_items.append(MenuItem(name="Blowout", price="150", description="Blast it to the moon"))
    p.menus[1].menu_items.append(MenuItem(name="Trim", price="25", description="Keep things neat and tidy"))
    p.menus[1].menu_items.append(MenuItem(name="Cut and Style", price="60", description="The full package"))

    p.gallery = Gallery()
    p.gallery.photos.append(Photo(url="http://placehold.it/300x300&text=1"))
    p.gallery.photos.append(Photo(url="http://placehold.it/300x300&text=2"))
    p.gallery.photos.append(Photo(url="http://placehold.it/500x500&text=3"))
    p.gallery.photos.append(Photo(url="http://placehold.it/678x300&text=4"))
    p.gallery.photos.append(Photo(url="http://placehold.it/300x300&text=5"))
    p.gallery.photos.append(Photo(url="http://placehold.it/1300x300&text=6"))
    p.gallery.photos.append(Photo(url="http://placehold.it/300x300&text=7"))
    p.gallery.photos.append(Photo(url="http://placehold.it/300x300&text=9"))
    p.gallery.photos.append(Photo(url="http://placehold.it/300x300&text=10"))
    p.gallery.photos.append(Photo(url="http://placehold.it/300x300&text=11"))
    p.gallery.photos.append(Photo(url="http://placehold.it/300x300&text=12"))
    p.gallery.photos.append(Photo(url="http://placehold.it/600x780&text=13"))
    p.gallery.photos.append(Photo(url="http://placehold.it/300x300&text=14"))
    p.gallery.photos.append(Photo(url="http://placehold.it/300x300&text=15"))
    p.gallery.photos.append(Photo(url="http://placehold.it/640x480&text=16"))
    p.gallery.photos.append(Photo(url="http://placehold.it/640x480&text=17"))
    p.gallery.photos.append(Photo(url="http://placehold.it/640x480&text=18"))
    p.gallery.photos.append(Photo(url="http://placehold.it/300x300&text=19"))
    p.gallery.photos.append(Photo(url="http://placehold.it/300x300&text=20"))
    p.gallery.photos.append(Photo(url="http://placehold.it/300x300&text=21"))
    p.gallery.photos.append(Photo(url="http://placehold.it/300x300&text=22"))
    p.gallery.photos.append(Photo(url="http://placehold.it/300x300&text=23"))
    p.gallery.photos.append(Photo(url="http://placehold.it/300x300&text=24"))
    p.gallery.photos.append(Photo(url="http://placehold.it/300x300&text=25"))
    p.gallery.photos.append(Photo(url="http://placehold.it/300x300&text=26"))
    p.gallery.photos.append(Photo(url="http://placehold.it/300x300&text=27"))
    p.gallery.photos.append(Photo(url="http://placehold.it/300x300&text=28"))
    p.gallery.photos.append(Photo(url="http://placehold.it/300x300&text=29"))

    db.session.add(p)

    # Consumer
    c = Consumer(user=ud.create_user(email='oneofy@gmail.com', password=password,
            first_name='Bob', last_name='Johnson'))
    c.user.confirmed_at = datetime.date.today()
    c.consumer_url = 'bob.johnson'
    db.session.add(c)
    db.session.commit()

@m.command
def create_index(doc_type):
    """Create new index and mapped doc_type
    """
    indexer.create_index(doc_type)

@m.command
def reset_index(doc_type):
    """Delete and recreate the index with doc_type
    """
    indexer.reset_index(doc_type)

def _build_menus():
    """Return a list of two menus, on barber and on salon
    composed of a random set of menu items
    """
    menus = []
    menus.append(Menu(menu_type="barbershop"))
    menus.append(Menu(menu_type="salon"))
    services = [
            'hair cut',
            'perm',
            'hair trim',
            'texturizer',
            'relaxer',
            'color',
            'color correction',
            'extensions',
            'weave',
            'wax',
            'blowout'
            ]
    prices = ['4', '15', '25', '17.99', '50.89', '55', '22']
    for i in range(5, random.randint(6, 15)):
        menus[0].menu_items.append(MenuItem(
            name=random.choice(services),
            price=random.choice(prices)
            )
            )
        menus[0].menu_items.append(MenuItem(
            name=random.choice(services),
            price=random.choice(prices)
            )
            )
        return menus


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
            # clean and convert lat lon to decimal if DMS
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
    """Pass a csv file
    Helps if the csv exhibits a schema like the Provider model
    """
    entities = _consume_csv(filename)
    for entity in entities:
        p = Provider(business_name=entity.pop('business_name'))
        p.location = Location(lat=entity.pop('lat'), lon=entity.pop('lon'))
        p.address = Address(**entity)
        p.business_url = acceptable_url_string(p.business_name,
                Config.ACCEPTABLE_URL_CHARS)
        p.menus = _build_menus()
        db.session.add(p)
        db.session.commit()
        # TODO indexing it here
        resp = indexer.index_one(p, id=p.id)
        print resp


def _make_context():
    return dict(
            app=create_app(),
            db=db,
            ud=ud,
            User=User,
            Role=Role,
            Provider=Provider,
            Consumer=Consumer,
            Review=Review,
            Address=Address,
            Gallery=Gallery,
            Photo=Photo,
            Menu=Menu,
            p=Provider.query.get(4),
            c=Consumer.query.first(),
            jsoner=JSONEncoder(),
            pprint=pprint,
            es=indexer.es
            )

m.add_option('-c', '--config', dest='config', required=False)
m.add_option('-i', '--instance', dest='instance_path', required=False)
m.add_command('run', Server(port='9016'))
m.add_command('shell', Shell(make_context=_make_context))


if __name__ == '__main__':
    m.run()
