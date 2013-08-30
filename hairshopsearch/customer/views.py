from flask import Blueprint, render_template, redirect, url_for
from .models import Customer
from .forms import CustomerForm

customer = Blueprint('customer', __name__, url_prefix='/customer', 
        template_folder='templates')

@customer.route('/')
def index():
    return 'customer index'

@customer.route('/register', methods=['GET', 'POST'])
def register():
    form = CustomerForm()
    if form.validate_on_submit():

        return redirect(url_for('frontend.index'))
    return render_template('customer/register.html', form=form)

