from flask import Flask, render_template, session, flash, redirect, url_for
from freshHarvest import app

from freshHarvest.models import Person, Customer, CorporateCustomer


@app.route('/customer_dashboard')
def customer_dashboard():
    if 'user' in session and session.get('role') in ['customer', 'corporate_customer']:
        # Customer-only content
        return render_template('customer_dashboard.html')
    else:
        flash("Unauthorized access.")
        return redirect(url_for('login'))
      
@app.route('/profile')
def profile():
    if 'user' in session and session.get('role') in ['customer', 'corporate_customer']:
        # Fetch the customer based on the user role
        customer_id = session['user_id']
        
        if session['role'] == 'corporate_customer':
            # Fetch CorporateCustomer profile details
            customer = CorporateCustomer.query.filter_by(id=customer_id).first()

        else:
            # Fetch regular Customer profile details
            customer = Customer.query.filter_by(id=customer_id).first()

        
        if not customer : 
            flash("Customer not found.")
            return redirect(url_for('login'))
        
        print(customer) 
        return render_template('profile.html', customer=customer)
    else:
        flash("Unauthorized access.")
        return redirect(url_for('login'))