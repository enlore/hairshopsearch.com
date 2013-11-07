class Default():
    FILE_LOGGING = True
    S3_URL = 'https://s3-us-west-2.amazonaws.com/hairshopsearch-dev'


class DevConfig(Default):
    FILE_LOG = '/tmp/info.hairshopsearch.log'
    FILE_ERROR_LOG = '/tmp/error.hairshopsearch.log'
    SECRET_KEY = 'dev key'
    DEBUG = True
    DEBUG_TB_ENABLED = DEBUG
    DEBUG_TB_PROFILER_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    ACCEPTABLE_URL_CHARS = "abcdefghijklmnopqrstuvwxyz0123456789."

    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/hairshopsearch.db'
    SQLALCHEMY_ECHO = False

    WTF_CSRF_ENABLED = True

    MAIL_SERVER = 'smtp.mailgun.org'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'postmaster@hairshopsearch.com'
    MAIL_PASSWORD = '4potz4gocm60'

    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = True
    SECURITY_EMAIL_SENDER = 'hairshopsearch-services@hairshopsearch.com'
    SECURITY_CONFIRMABLE = True
    SECURITY_TRACKABLE = True
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = 'salty'
    SECURITY_RECOVERABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_POST_LOGIN_VIEW = '/dashboard/profile'
    SECURITY_POST_REGISTER_VIEW = '/welcome'

class Config(DevConfig):
    MAIL_LOGGING = True
    MAIL_LOG_FROM = ['HSS_APP_ERROR@hairshopsearch.com']
    MAIL_LOG_ADMINS = ['oneofy@gmail.com']
