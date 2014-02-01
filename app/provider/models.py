from flask import current_app
from ..helpers import JSONSerializer, acceptable_url_string
from ..core import db
from ..indexer.indexer import index_one

class ProviderSerializer(JSONSerializer):
    __json_hidden__ = [
            'gallery', 'avatar', 'products',
            'hours', 'user', 'favorited_by',
            'reviews', 'fb_url', 'links', 'twitter_url', 'phone',
            '_business_url', 'email', 'bio', 'address', 'payment_methods',
            'business_name', 'endorses', 'endorsed_by']


endorsers_endorsees = db.Table('endorsers_endorsees',
            db.Column('endorser', db.Integer, db.ForeignKey('provider.id'), primary_key=True),
            db.Column('endorsee', db.Integer, db.ForeignKey('provider.id'), primary_key=True)
        )


class Provider(db.Model, ProviderSerializer):
    _db = db

    def save(self):
        """
        Save an instance in the db
        """
        self._db.session.add(self)
        self._db.session.commit()

    @classmethod
    def get(cls, id):
        """
        Classmethod
        Get a model by it's id
        :param id: 
        :type id: integer
        :rtype: Provider obj
        """
        return cls.query.get(id)
    
    @classmethod
    def find(cls, **kwargs):
        """
        Find collection of models, qualifie by args
        """
        return cls.query.filter_by(**kwargs).all()

    def index(self):
        return index_one(self, self.id)

    def update_index(self):
        pass

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
        self._business_url = value

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

    menus               = db.relationship('Menu',
                            backref=db.backref('provider'))
    gallery             = db.relationship('Gallery', uselist=False)
    products            = db.relationship('Product', backref='provider')
    location            = db.relationship('Location', uselist=False)
    endorses            = db.relationship('Provider',
                            secondary=endorsers_endorsees,
                            primaryjoin=id==endorsers_endorsees.c.endorser,
                            secondaryjoin=id==endorsers_endorsees.c.endorsee,
                            backref="endorsed_by")


class ProviderInstance(db.Model):
    __tablename__      = 'provider_instance'

    name                = db.Column(db.String, primary_key=True)
    count               = db.Column(db.Integer)


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


class MenuSerializer(JSONSerializer):
    __json_hidden__ = ['provider', 'provider_id', 'id']


class Menu(db.Model, MenuSerializer):
    id                  = db.Column(db.Integer, primary_key=True)
    provider_id         = db.Column(db.Integer, db.ForeignKey('provider.id'))
    menu_type           = db.Column(db.String)
    menu_items          = db.relationship('MenuItem', backref='menu')


class MenuItemSerializer(JSONSerializer):
    __json_hidden__ = ['menu', 'menu_id', 'id']


class MenuItem(db.Model, MenuItemSerializer):
    id                  = db.Column(db.Integer, primary_key=True)
    menu_id             = db.Column(db.Integer, db.ForeignKey('menu.id'))
    name                = db.Column(db.String)
    price               = db.Column(db.Float(precision=2))
    description         = db.Column(db.Text())


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


