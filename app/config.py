class Default():
    FILE_LOGGING = True


class DevConfig(Default):
    SECRET_KEY = 'dev key'
    DEBUG = True


class Config(DevConfig):
    pass
