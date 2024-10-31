from flask import Flask, render_template, session, flash, redirect, url_for, request, jsonify
from freshHarvest import app,db
from freshHarvest.models import  CorporateCustomer, Customer, PremadeBox, Order,Payment,Person,OrderLine,Item
from sqlalchemy.orm import aliased
from collections import Counter
from datetime import datetime
from sqlalchemy import func

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
  
 
@app.route('/report')
def report():
    return render_template('sales_report.html') 


@app.route('/api/sales_data')
def sales_data():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Fetch sales data for the specified period
    sales_data = (
        db.session.query(Order, OrderLine, Item)
        .join(OrderLine, OrderLine.order_id == Order.id)  # Join OrderLine with Order
        .join(Item, OrderLine.item_id == Item.id)  # Join Item with OrderLine
        .filter(Order.date.between(start_date, end_date))
        .all()
    )

    print("sales_data", sales_data)

    # Aggregate sales by date
    sales_summary = {}
    item_counts = Counter()
    
    for order, order_line, item in sales_data:
        date = order.date.strftime('%Y-%m-%d')
        quantity = order_line.quantity
        item_name = item.name
        total_price = order_line.quantity * item.price  # Assuming item has a price attribute

        # Update sales summary with both quantity and revenue
        if date not in sales_summary:
            sales_summary[date] = {'quantity': 0, 'revenue': 0}
        
        sales_summary[date]['quantity'] += quantity
        sales_summary[date]['revenue'] += total_price
        item_counts[item_name] += quantity

    # Find the most popular item
    if item_counts:
        most_popular_item, max_quantity = item_counts.most_common(1)[0]
    else:
        most_popular_item, max_quantity = None, 0

    response = {
        "labels": list(sales_summary.keys()),
        "totals_quantity": [v['quantity'] for v in sales_summary.values()],
        "totals_revenue": [v['revenue'] for v in sales_summary.values()],
        "most_popular_item": most_popular_item,
        "max_quantity": max_quantity
    }

    return jsonify(response)
