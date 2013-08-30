from ..extensions import db

class Customer(db.Model):
    id                  = db.Column(db.Integer, primary_key=True)
    user                = db.relationship('User', backref='customer', uselist=False)
    # providers_favd
    # comments left

