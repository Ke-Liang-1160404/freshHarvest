from flask import Flask, render_template, session, flash, redirect, url_for
from freshHarvest import app,db
from freshHarvest.models import  CorporateCustomer, Customer, PremadeBox, Order,Payment,Person
from sqlalchemy.orm import aliased

@app.route('/staff_dashboard')
def staff_dashboard():
    if 'user' in session and session.get('role') == 'staff':
        # Staff-only content
        return render_template('staff_dashboard.html')
    else:
        flash("Unauthorized access.")
        return redirect(url_for('login'))



@app.route('/all_customers')
def all_customers():

    CorporateCustomerAlias = aliased(CorporateCustomer)

    # Query all customers, joining CorporateCustomer if available
    customers = (
        db.session.query(Customer, CorporateCustomerAlias)
        .outerjoin(CorporateCustomerAlias, Customer.id == CorporateCustomerAlias.id)
        .all()
    )

    # Process data to output in one combined format
    results = [
        {
            'customer_id': customer.id,
            'first_name': customer.first_name,
            'last_name': customer.last_name,
            'username': customer.username,
            'balance': customer.balance,
            'max_owing': customer.max_owing,
            'is_corporate': corporate_customer is not None,
            'discount_rate': corporate_customer.discount_rate if corporate_customer else None,
            'credit_limit': corporate_customer.credit_limit if corporate_customer else None,
            'min_balance': corporate_customer.min_balance if corporate_customer else None
        }
        for customer, corporate_customer in customers
    ]

    print(results)
    return render_template('all_customers.html', results= results) 
  
  
  
@app.route('/all_orders')
def all_orders():
    # Query all orders
    customer_id=session['user_id']
    # Retrieve all orders for the customer and their payment information
    orders = db.session.query(Order, Payment, Person
    ).join(
        Payment, Order.id == Payment.id, isouter=True

    ).join(Person, Order.customer_id == Person.id, isouter=True 
    ).all()
    return render_template('all_orders.html', orders=orders)  
  
  
@app.route('/customer/<int:id>')
def see_customer(id):
    orders = db.session.query(Order, Payment, Person
    ).join(
        Payment, Order.id == Payment.id, isouter=True
    ).join(Person, Order.customer_id == Person.id, isouter=True
    ).filter(
        Order.customer_id == id
    ).all()
    
    print(orders)

    return render_template('orders.html', orders=orders)