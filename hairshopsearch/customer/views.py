from flask import Blueprint, render_template, redirect, url_for
from .models import Customer
from .forms import CustomerForm
from ..user.models import User
from ..extensions import db

customer = Blueprint('customer', __name__, url_prefix='/customer', 
        template_folder='templates')

@customer.route('/')
def index():
    return 'customer index'

@customer.route('/register', methods=['GET', 'POST'])
def register():
    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customer()
        form.populate_obj(customer)
        
        customer.user = User()
        form.populate_obj(customer.user)

        db.session.add(customer)
        db.session.commit()

        return redirect(url_for('frontend.index'))
    return render_template('customer/register.html', form=form)

