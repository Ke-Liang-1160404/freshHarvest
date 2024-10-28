#import 
from flask import render_template, request, redirect, url_for, session,flash
from flask_hashing import Hashing
from freshHarvest import db, app

from freshHarvest.models import PeopleModels, ProductModels, OrderPaymentModels
from flask_hashing import Hashing

hashing= Hashing(app)
hashing_salt="freshHarvest"

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.pop('user', None)
        
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashing.hash_value(password, hashing_salt)
        
        # Find user by username
        user =PeopleModels.Person.query.filter_by(username=username).first()
        
        if user:
            # Check password
            is_valid = hashing.check_value(user.password, password, hashing_salt)
            
            if is_valid:
                # Set session and role based on user type
                session['user'] = user.username
                staff_user = PeopleModels.Staff.query.filter_by(id=user.id).first()
                if staff_user:
                    session['role'] = 'staff'
                # Check if the user is a CorporateCustomer
                elif PeopleModels.CorporateCustomer.query.filter_by(id=user.id).first():
                    session['role'] = 'corporate_customer'
                # Check if the user is a Customer
                elif PeopleModels.Customer.query.filter_by(id=user.id).first():
                    session['role'] = 'customer'

                # Redirect based on role
                if session['role'] == 'staff':
                    return redirect(url_for('staff_dashboard',session=session))
                elif session['role'] == 'corporate_customer':
                    return redirect(url_for('customer_dashboard',session=session))
                elif session['role'] == 'customer':
                    return redirect(url_for('customer_dashboard',session=session))



 
            else:
                flash("Incorrect password, please try again.")
        else:
            flash("Username not found, please try again.")
        
    return render_template('login.html')
  
  
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('role', None)
    return redirect(url_for('login'))
  
@app.route('/all_customers')
def all_customers():
  
    customers= PeopleModels.Customer.query.all()
    staff=PeopleModels.Staff.query.all()
    corporate=PeopleModels.CorporateCustomer.query.all()
    order=OrderPaymentModels.Order.query.all()
    payment=OrderPaymentModels.Payment.query.all()
    creditsCards= OrderPaymentModels.CreditCardPayment.query.all()
    debitCards=OrderPaymentModels.DebitCardPayment.query.all()
    item=ProductModels.Item.query.all()
    veggie=ProductModels.Veggie.query.all()
    box=ProductModels.PremadeBox.query.all()
    contents=ProductModels.PremadeBox.query.all()
    print(customers)
    print(staff,"/n",corporate,"/n",order,"/n",payment,"/n",creditsCards,"/n",debitCards,"/n",item,"/n",veggie,"/n",box,"/n",contents)
    return render_template('base.html', customers= customers) 