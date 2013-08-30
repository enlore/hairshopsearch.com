from ..extensions import db

class SalonManager(db.Model):

    id              = db.Column(db.Integer, primary_key=True)
    avatar          = db.Column(db.String(256))
    hours           = db.Column(db.String(256))
    phone           = db.Column(db.String(32),unique=True)
    business_name   = db.Column(db.String(256))
    street_address  = db.Column(db.String(256))
    city            = db.Column(db.String(128))
    state           = db.Column(db.String(16))
    zip_code        = db.Column(db.String(16))
    user            = db.relationship('User', backref='salon_manager', uselist=False) 
    stylists        = db.relationship('Stylist', backref='salon',
            lazy='dynamic')

    def __init__(self):
        self.active = True
