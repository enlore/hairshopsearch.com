class Default():
    FILE_LOGGING = True


class DevConfig(Default):
    FILE_LOG = '/tmp/hairshopsearch.info.log'
    SECRET_KEY = 'dev key'
    DEBUG = True
    DEBUG_TB_PROFILER_ENABLED = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/hairshopsearch.db'
    SQLALCHEMY_ECHO = True

    WTF_CSRF_ENABLED = True

    MAIL_SERVER = 'smtp.mailgun.org'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'postmaster@hairshopsearch.com'
    MAIL_PASSWORD = '4potz4gocm60'

    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = True
    SECURITY_EMAIL_SENDER = 'services@hairshopsearch.com'
    SECURITY_CONFIRMABLE = True
    SECURITY_TRACKABLE = True
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = 'salty'
    SECURITY_RECOVERABLE = True
    SECURITY_CHANGEABLE = True

class Config(DevConfig):
    pass
