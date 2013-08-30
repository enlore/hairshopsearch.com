from ..extensions import db
from werkzeug import generate_password_hash, check_password_hash
from ..util import ROLES

class User(db.Model):
    id                  = db.Column(db.Integer, primary_key=True)
    email               = db.Column(db.String(256), unique=True)
    first_name          = db.Column(db.String(128))
    last_name           = db.Column(db.String(128))
    salonmanager_id     = db.Column(db.Integer, db.ForeignKey('salon_manager.id'))
    stylist_id          = db.Column(db.Integer, db.ForeignKey('stylist.id'))
    customer_id         = db.Column(db.Integer,
            db.ForeignKey('customer.id'))
     
    _password   = db.Column(db.String(), nullable=False)

    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def _check_password(password):
        if password is None:
            return False
        return check_password_hash(self._password, password)

    # customer, salon manager, stylist, product vendor
    _role_code  = db.Column(db.Integer(8))

    @property
    def role(self):
        return ROLES[this._role_code]

    @role.setter
    def role(self, role):
        self._role_code = role

    # active? 
    _status     = db.Column(db.Integer())

    @property
    def active(self):
        return self._status

    @active.setter
    def active(self, value):
        self._status = value


    def is_authenticated():
        pass

    def is_anonymous():
        pass

    def is_active(self):
        return self.active or None

    def get_id(self, user):
        return user.id

    def __repr__(self):
        return '<User> %s, %s, %s, %s' % (self.id, self.email, self.first_name,
                self.password)
