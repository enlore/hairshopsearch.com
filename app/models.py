from flask import current_app
from flask.ext.security import UserMixin, RoleMixin
from sqlalchemy.ext.hybrid import hybrid_property
from .core import db
from .helpers import JSONSerializer, acceptable_url_string

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
    gender              = db.Column(db.String)
    birth_day           = db.Column(db.DateTime)
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


class ReviewSerializer(JSONSerializer):
    __json_hidden__ = ['user', 'provider']


class Review(db.Model, ReviewSerializer):
    id                  = db.Column(db.Integer, primary_key=True)
    user_id             = db.Column(db.Integer, db.ForeignKey('user.id'))
    provider_id         = db.Column(db.Integer, db.ForeignKey('provider.id'))
    body                = db.Column(db.Text)


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
    hair_routine_id     = db.Column(db.Integer, db.ForeignKey('hairroutine.id'))


consumers_providers = db.Table('consumers_providers',
        db.Column('consumer_id', db.Integer, db.ForeignKey('consumer.id')),
        db.Column('provider_id', db.Integer, db.ForeignKey('provider.id'))
        )

followers_followed = db.Table('followers_followed',
            db.Column('follower', db.Integer, db.ForeignKey('consumer.id'), primary_key=True),
            db.Column('followed', db.Integer, db.ForeignKey('consumer.id'), primary_key=True)
        )

class Consumer(db.Model, JSONSerializer):
    id                  = db.Column(db.Integer, primary_key=True)
    user                = db.relationship('User', backref='consumer',
                            uselist=False)
    _consumer_url       = db.Column(db.String)
    favorites           = db.relationship('Provider',
                            backref=db.backref('favorited_by', lazy='dynamic'),
                            secondary=consumers_providers)
    blog_url            = db.Column(db.String)
    fb_url              = db.Column(db.String)
    gplus_url           = db.Column(db.String)
    youtube_url         = db.Column(db.String)
    vimeo_url           = db.Column(db.String)
    other_url           = db.Column(db.String)
    avatar              = db.relationship('Photo', uselist=False)
    bio                 = db.Column(db.Text)
    location            = db.Column(db.String)
    hair_articles       = db.relationship('Article')
    hair_routine        = db.relationship('HairRoutine', backref= 'consumer',
                            uselist=False)
    follows             = db.relationship('Consumer',
                            secondary=followers_followed,
                            primaryjoin=id==followers_followed.c.follower,
                            secondaryjoin=id==followers_followed.c.followed,
                            backref='followers')

    @hybrid_property
    def consumer_url(self):
        return self._consumer_url

    @consumer_url.setter
    def consumer_url(self, value):
        self._consumer_url = value


class HairRoutineSerializer(JSONSerializer):
    __json_hidden__ = [
            'hair_condition',
            'chemical_treat',
            'last_treatment',
            'fav_style',
            'shampoo_type',
            'shampoo_frequency',
            'conditioner_type',
            'scalp_condition',
            'last_trim',
            'fav_products'
            ]


class HairRoutine(db.Model, HairRoutineSerializer):
    __tablename__       = 'hairroutine'
    id                  = db.Column(db.Integer, primary_key=True)
    consumer_id         = db.Column(db.Integer, db.ForeignKey('consumer.id'))
    hair_condition      = db.Column(db.String()) # text
    chemical_treat      = db.Column(db.Boolean()) # bool
    last_treatment      = db.Column(db.String()) # text
    fav_style           = db.Column(db.String()) # text
    shampoo_type        = db.Column(db.String()) # text
    shampoo_frequency   = db.Column(db.String()) # string
    conditioner_type    = db.Column(db.String()) # string
    condition_frequency = db.Column(db.String()) # string
    scalp_condition     = db.Column(db.String())
    last_trim           = db.Column(db.String())
    favorite_products   = db.relationship('Product')


class ConsumerInstance(db.Model):
    __tablename__      = 'consumer_instance'

    name                = db.Column(db.String, primary_key=True)
    count               = db.Column(db.Integer)
