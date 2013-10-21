from flask import current_app
from flask.ext.security import UserMixin, RoleMixin
from ..core import db
from ..helpers import JSONSerializer, acceptable_url_string

# association object
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
        )


class Role(db.Model, RoleMixin):
    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String(), unique=True)
    description     = db.Column(db.String())


class User(db.Model, UserMixin):
    id                  = db.Column(db.Integer, primary_key=True)
    provider_id         = db.Column(db.Integer, db.ForeignKey('provider.id'))
    consumer_id         = db.Column(db.Integer, db.ForeignKey('consumer.id'))
    first_name          = db.Column(db.String)
    last_name           = db.Column(db.String)
    email               = db.Column(db.String(), unique=True)
    password            = db.Column(db.String())
    active              = db.Column(db.Boolean())
    confirmed_at        = db.Column(db.DateTime())
    current_login_at    = db.Column(db.DateTime())
    last_login_at       = db.Column(db.DateTime())
    current_login_ip    = db.Column(db.String())
    last_login_ip       = db.Column(db.String())
    login_count         = db.Column(db.Integer())
    roles               = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('user', lazy='dynamic'))

    reviews             = db.relationship('Review', backref=db.backref('user'))


class AddressSerializer(JSONSerializer):
    __json_hidden__ = ['provider']


class Address(db.Model, AddressSerializer):
    id                  = db.Column(db.Integer, primary_key=True)
    provider_id         = db.Column(db.Integer, db.ForeignKey('provider.id'))
    street_1            = db.Column(db.String)
    street_2            = db.Column(db.String)
    apartment           = db.Column(db.String)
    city                = db.Column(db.String)
    state               = db.Column(db.String)
    zip_code            = db.Column(db.Integer)

    def __repr__(self):
        return '%s %s %s, %s, %s %s' %(
               self.street_1,
               self.street_2,
               self.apartment,
               self.city,
               self.state,
               self.zip_code
                )


class ReviewSerializer(JSONSerializer):
    __json_hidden__ = ['user', 'provider']


class Review(db.Model, ReviewSerializer):
    id                  = db.Column(db.Integer, primary_key=True)
    user_id             = db.Column(db.Integer, db.ForeignKey('user.id'))
    provider_id         = db.Column(db.Integer, db.ForeignKey('provider.id'))
    body                = db.Column(db.Text)


class MenuSerializer(JSONSerializer):
    __json_hidden__ = ['provider', 'provider_id', 'id']


class Menu(db.Model, MenuSerializer):
    id                  = db.Column(db.Integer, primary_key=True)
    provider_id         = db.Column(db.Integer, db.ForeignKey('provider.id'))
    menu_type           = db.Column(db.String)
    menu_items          = db.relationship('MenuItem', backref='menu')


class MenuItemSerializer(JSONSerializer):
    __json_hidden__ = ['menu']


class MenuItem(db.Model, MenuItemSerializer):
    id                  = db.Column(db.Integer, primary_key=True)
    menu_id             = db.Column(db.Integer, db.ForeignKey('menu.id'))
    name                = db.Column(db.String)
    price               = db.Column(db.Float(precision=2))


class Photo(db.Model):
    id                  = db.Column(db.Integer, primary_key=True)
    url                 = db.Column(db.Text)
    provider_id         = db.Column(db.Integer, db.ForeignKey('provider.id'))
    gallery_id          = db.Column(db.Integer, db.ForeignKey('gallery.id'))
    consumer_id         = db.Column(db.Integer, db.ForeignKey('consumer.id'))


class Gallery(db.Model):
    id                  = db.Column(db.Integer, primary_key=True)
    provider_id         = db.Column(db.Integer, db.ForeignKey('provider.id'))
    photos              = db.relationship('Photo', backref='gallery')


class ArticleSerializer(JSONSerializer):
    __json_hidden__ = ['consumer']


class Article(db.Model, ArticleSerializer):
    id                  = db.Column(db.Integer, primary_key=True)
    consumer_id         = db.Column(db.Integer, db.ForeignKey('consumer.id'))
    body                = db.Column(db.Text)
    title               = db.Column(db.String)


class ProductSerializer(JSONSerializer):
    __json_hidden__ = ['consumer', 'provider']


class Product(db.Model, JSONSerializer):
    id                  = db.Column(db.Integer, primary_key=True)
    name                = db.Column(db.String)
    description         = db.Column(db.String)
    provider_id         = db.Column(db.Integer, db.ForeignKey('provider.id'))
    consumer_id         = db.Column(db.Integer, db.ForeignKey('consumer.id'))


class HoursSerializer(JSONSerializer):
    __json_hidden__ = ['provider']


class Hours(db.Model, HoursSerializer):
    id                      = db.Column(db.Integer, primary_key=True)
    provider_id             = db.Column(db.Integer,
                                db.ForeignKey('provider.id'))
    monday_open             = db.Column(db.String)
    monday_close            = db.Column(db.String)
    tuesday_open            = db.Column(db.String)
    tuesday_close           = db.Column(db.String)
    wednesday_open          = db.Column(db.String)
    wednesday_close         = db.Column(db.String)
    thursday_open           = db.Column(db.String)
    thursday_close          = db.Column(db.String)
    friday_open             = db.Column(db.String)
    friday_close            = db.Column(db.String)
    saturday_open           = db.Column(db.String)
    saturday_close          = db.Column(db.String)
    sunday_open             = db.Column(db.String)
    sunday_close            = db.Column(db.String)


class LocationSerializer(JSONSerializer):
    __json_hidden__ = ['provider_id', 'id']

class Location(db.Model, LocationSerializer):
    id              = db.Column(db.Integer, primary_key=True)
    provider_id     = db.Column(db.Integer, db.ForeignKey('provider.id'))
    lat             = db.Column(db.Float)
    lon             = db.Column(db.Float)


consumers_providers = db.Table('consumers_providers',
        db.Column('consumer_id', db.Integer, db.ForeignKey('consumer.id')),
        db.Column('provider_id', db.Integer, db.ForeignKey('provider.id'))
        )

class ProviderSerializer(JSONSerializer):
    __json_hidden__ = [
            'gallery', 'avatar', 'products',
            'hours', 'user', 'favorited_by',
            'reviews', 'fb_url', 'links', 'twitter_url', 'phone',
            '_business_url', 'email', 'bio', 'address', 'payment_methods',
            'business_name']

class Provider(db.Model, ProviderSerializer):
    id                  = db.Column(db.Integer, primary_key=True)
    user                = db.relationship('User', backref='provider',
                            uselist=False)

    avatar              = db.relationship('Photo', uselist=False)

    business_name       = db.Column(db.String)
    _business_url       = db.Column(db.String)

    @property
    def business_url(self):
        return self._business_url

    @business_url.setter
    def business_url(self, value):
        test_string = acceptable_url_string(
                value,
                current_app.config['ACCEPTABLE_URL_CHARS'])

        like_string = '{}%'.format(test_string)

        count = Provider.query.filter(
                Provider._business_url.like(like_string)).count()

        proper_url = '{}-{}'.format(test_string, count)

        self._business_url = proper_url

    phone               = db.Column(db.String)
    email               = db.Column(db.String)
    hours               = db.relationship('Hours', uselist=False)
    address             = db.relationship('Address', uselist=False,
                            backref=db.backref('provider'))
    payment_methods     = db.Column(db.String, default='')

    bio                 = db.Column(db.Text)
    fb_url              = db.Column(db.String)
    twitter_url         = db.Column(db.String)
    links               = db.Column(db.String)

    reviews             = db.relationship('Review',
                            backref=db.backref('provider'))
    menus               = db.relationship('Menu',
                            backref=db.backref('provider'))
    gallery             = db.relationship('Gallery', uselist=False)
    products            = db.relationship('Product', backref='provider')
    location            = db.relationship('Location', uselist=False)

class Consumer(db.Model, JSONSerializer):
    id                  = db.Column(db.Integer, primary_key=True)
    user                = db.relationship('User', backref='consumer',
                            uselist=False)
    hair_type           = db.Column(db.String)
    hair_products       = db.relationship('Product', backref='consumer')
    hair_routine        = db.Column(db.Text)
    favorites           = db.relationship('Provider',
                            backref=db.backref('favorited_by', lazy='dynamic'),
                            secondary=consumers_providers)
    links               = db.Column(db.String)
    avatar              = db.relationship('Photo', uselist=False)
    bio                 = db.Column(db.Text)
    hair_articles       = db.relationship('Article')


class ConsumerInstance(db.Model):
    __table_name__      = 'consumer_instance'

    name                = db.Column(db.String, primary_key=True)
    count               = db.Column(db.Integer)
