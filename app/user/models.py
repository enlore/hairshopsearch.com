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
    id              = db.Column(db.Integer, primary_key=True)
    provider_id         = db.Column(db.Integer, db.ForeignKey('provider.id'))
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
    id              = db.Column(db.Integer, primary_key=True)
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
    menu_type           = db.Column(db.String)
    menu_pickle         = db.Column(db.PickleType)

    provider_id         = db.Column(db.Integer, db.ForeignKey('provider.id'))


class Photo(db.Model):
    id                  = db.Column(db.Integer, primary_key=True)
    url                 = db.Column(db.Text)
    provider_id         = db.Column(db.Integer, db.ForeignKey('provider.id'))
    gallery_id          = db.Column(db.Integer, db.ForeignKey('gallery.id'))


class Gallery(db.Model):
    id                  = db.Column(db.Integer, primary_key=True)
    provider_id         = db.Column(db.Integer, db.ForeignKey('provider.id'))
    photos              = db.relationship('Photo', backref='gallery')


class Provider(db.Model):
    id                  = db.Column(db.Integer, primary_key=True)
    user                = db.relationship('User', backref='provider', 
                            uselist=False)
    business_name       = db.Column(db.String)
    bio                 = db.Column(db.Text)
    fb_url              = db.Column(db.String)
    twitter_url         = db.Column(db.String)
    email               = db.Column(db.String)
    hours               = db.Column(db.PickleType)
    payment_methods     = db.Column(db.String)
    links               = db.Column(db.String)
    
    address             = db.relationship('Address', uselist=False,
                            backref=db.backref('provider'))
    
    avatar              = db.relationship('Photo', uselist=False)

    reviews             = db.relationship('Review',
                            backref=db.backref('provider'))
    
    menus               = db.relationship('Menu',
                            backref=db.backref('provider'))
    
    gallery             = db.relationship('Gallery', uselist=False)
