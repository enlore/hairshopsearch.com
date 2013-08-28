from flask.ext.sqlalchemy import db
from werkzeug import create_password_hash, check_password_hash
from ..util import ROLES

class User():
    id          = db.Column(db.Integer, primary_key=True)
    email       = db.Column(db.String(256), unique=True)
    first_name  = db.Column(db.String(128))
    last_name   = db.Column(db.String(128))
     
    _password   = db.Column(db.String())

    # customer, salon manager, stylist, product vendor
    _role_code  = db.Column(db.Integer())

    # active? 
    _status     = db.Column(db.Integer())

    @proptery
    def role(self):
        return ROLES[this._role_code]

    @role.setter
    def role(self, role):
        pass

    @property
    def active(self):
        return self._status


    def is_authenticated():
        pass

    def is_anonymous():
        pass

    def is_active(self):
        return self.active or None

    def get_id():
        pass
