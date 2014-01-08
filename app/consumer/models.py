from flask import current_app
from sqlalchemy.ext.hybrid import hybrid_property
from ..core import db
from ..helpers import JSONSerializer, acceptable_url_string

followers_followed = db.Table('followers_followed',
            db.Column('follower', db.Integer, db.ForeignKey('consumer.id'), primary_key=True),
            db.Column('followed', db.Integer, db.ForeignKey('consumer.id'), primary_key=True)
        )

consumers_providers = db.Table('consumers_providers',
        db.Column('consumer_id', db.Integer, db.ForeignKey('consumer.id')),
        db.Column('provider_id', db.Integer, db.ForeignKey('provider.id'))
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
    hair_routine        = db.relationship('HairRoutine', backref= 'consumer',
                            uselist=False)
    follows             = db.relationship('Consumer',
                            secondary=followers_followed,
                            primaryjoin=id==followers_followed.c.follower,
                            secondaryjoin=id==followers_followed.c.followed,
                            backref='followers')
    gallery             = db.relationship('Gallery', uselist=False)

    @hybrid_property
    def consumer_url(self):
        return self._consumer_url

    @consumer_url.setter
    def consumer_url(self, value):
        self._consumer_url = value


class ConsumerInstance(db.Model):
    __tablename__      = 'consumer_instance'

    name                = db.Column(db.String, primary_key=True)
    count               = db.Column(db.Integer)


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
    chemical_treat      = db.Column(db.String()) # bool
    last_treatment      = db.Column(db.String()) # text
    fav_style           = db.Column(db.String()) # text
    shampoo_type        = db.Column(db.String()) # text
    shampoo_frequency   = db.Column(db.String()) # string
    conditioner_type    = db.Column(db.String()) # string
    condition_frequency = db.Column(db.String()) # string
    scalp_condition     = db.Column(db.String())
    last_trim           = db.Column(db.String())
    favorite_products   = db.relationship('Product')
