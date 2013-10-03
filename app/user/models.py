from flask.ext.security import UserMixin, RoleMixin
from ..core import db

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


class Address(db.Model):
    id                  = db.Column(db.Integer, primary_key=True)
    provider_id         = db.Column(db.Integer, db.ForeignKey('provider.id'))
    street_1            = db.Column(db.String)
    street_2            = db.Column(db.String)
    apartment           = db.Column(db.String)
    city                = db.Column(db.String)
    state               = db.Column(db.String)
    zip_code            = db.Column(db.Integer)


class Review(db.Model):
    id                  = db.Column(db.Integer, primary_key=True)
    user_id             = db.Column(db.Integer, db.ForeignKey('user.id'))
    provider_id         = db.Column(db.Integer, db.ForeignKey('provider.id'))
    body                = db.Column(db.Text)


class Menu(db.Model):
    id                  = db.Column(db.Integer, primary_key=True)
    provider_id         = db.Column(db.Integer, db.ForeignKey('provider.id'))
    menu_type           = db.Column(db.String)
    menu_items          = db.relationship('MenuItem', backref='menu')


class MenuItem(db.Model):
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


class Article(db.Model):
    id                  = db.Column(db.Integer, primary_key=True)
    consumer_id         = db.Column(db.Integer, db.ForeignKey('consumer.id'))
    body                = db.Column(db.Text)
    title               = db.Column(db.String)


class Product(db.Model):
    id                  = db.Column(db.Integer, primary_key=True)
    name                = db.Column(db.String)
    description         = db.Column(db.String)
    provider_id         = db.Column(db.Integer, db.ForeignKey('provider.id'))
    consumer_id         = db.Column(db.Integer, db.ForeignKey('consumer.id'))


consumers_providers = db.Table('consumers_providers',
        db.Column('consumer_id', db.Integer, db.ForeignKey('consumer.id')),
        db.Column('provider_id', db.Integer, db.ForeignKey('provider.id'))
        )

class Provider(db.Model):
    id                  = db.Column(db.Integer, primary_key=True)
    user                = db.relationship('User', backref='provider',
                            uselist=False)

    avatar              = db.relationship('Photo', uselist=False)

    business_name       = db.Column(db.String)
    phone               = db.Column(db.String)
    email               = db.Column(db.String)
    hours               = db.Column(db.PickleType, default={})
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


class Consumer(db.Model):
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


