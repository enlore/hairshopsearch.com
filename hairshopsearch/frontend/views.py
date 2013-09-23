# -*- encoding: utf-8 -*-
from flask import Blueprint, render_template

frontend = Blueprint('frontend', __name__, template_folder='templates')

@frontend.route('/')
def index():
    return 'index yo'
