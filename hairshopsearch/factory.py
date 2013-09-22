from flask import Flask

def create_app(config=None):
    app = Flask('hairshopsearch')
    return app
