from ..extensions import db

class Stylist(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    avatar      = db.Column(db.String(256))
    blurb       = db.Column(db.String(500))
    user        = db.relationship('User', backref='stylist', uselist=False)
    salon_manager_id    = db.Column(db.Integer(2),
            db.ForeignKey('salon_manager.id'))
    
    def __init__(self):
        self.active = True
