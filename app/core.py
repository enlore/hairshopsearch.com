from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask.ext.security import SQLAlchemyUserDatastore
from app.user.models import User, Role
ud = SQLAlchemyUserDatastore(db, User, Role)

from flask.ext.mail import Mail
mail = Mail()

from pyelasticsearch import ElasticSearch
es = ElasticSearch('http://localhost:9200')

class HSSError(Exception):
    def __init__(self, msg):
        self.msg = msg
