# -*- encoding: utf-8 -*-
from flask import Blueprint, render_template
from ..stylist.models import Stylist
from ..salonmanager.models import SalonManager

frontend = Blueprint('frontend', __name__, template_folder='templates')

@frontend.route('/')
def index():
    stylists = Stylist.query.all()
    s_ms = SalonManager.query.all()
    return render_template('index.html',stylists=stylists, s_ms = s_ms)
