from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from flask.ext.security import SQLAlchemyUserDatastore, Security
from app.user.models import User, Role

security = Security()
ud = SQLAlchemyUserDatastore(db, User, Role)

from flask.ext.mail import Mail
mail = Mail()
