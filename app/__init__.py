from .factory import _create_app

def create_app(config=None):
    return _create_app(__name__, __path__, config)
