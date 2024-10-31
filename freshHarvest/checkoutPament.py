from flask import render_template, request, redirect, url_for, flash,session,jsonify
from freshHarvest import db, app
from freshHarvest.models import Order,OrderLine, Payment, CreditCardPayment, DebitCardPayment, Customer, CorporateCustomer, Person,Item
from datetime import datetime
from sqlalchemy.orm import aliased

# Create aliases for each 'person' reference
PersonAlias1 = aliased(Person)
PersonAlias2 = aliased(Person)


@app.route('/orders')
def orders():
    customer_id=session['user_id']
    # Retrieve all orders for the customer and their payment information
    orders = db.session.query(Order, Payment, Person
    ).join(
        Payment, Order.id == Payment.id, isouter=True
    ).join(Person, Order.customer_id == Person.id, isouter=True
    ).filter(
        Order.customer_id == customer_id
    ).all()
  


    return render_template('orders.html', orders=orders)

@app.route('/order/<int:order_id>')
def order_detail(order_id):

    order_lines = (
                OrderLine.query
                .join(Item, OrderLine.item_id == Item.id)
                .add_columns(Item.name, Item.type, Item.price)
                .filter(OrderLine.order_id == order_id)
                .all()
            ) 
    print("order_lines",order_lines)
      # Convert order_lines to a list of dictionaries
    order_lines_data = [{
        'name': item_name,
        'type': type,
        'price': price,
        'quantity': order_line.quantity ,
        'total': order_line.order_line_total()  
    } for order_line, item_name, type, price in order_lines]
    print("order_lines_data",order_lines_data)
    return jsonify(order_lines=order_lines_data)
  


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    customer_id = session.get('user_id')

    if not customer_id:
        flash("Please log in to proceed with checkout.")
        return redirect(url_for('login'))

    # Retrieve the pending order for the customer
    order = Order.query.filter_by(customer_id=customer_id, status='Pending').first()
    if not order:
        flash("No pending order found.")
        return redirect(url_for('products'))

    # Check if the customer is a corporate customer and apply discount
    is_corporate_customer = session.get('role') == 'corporate_customer'
    discount_rate = 0.1  # Default 10% discount for corporate customers
    original_total = order.order_total()

    # Apply discount if corporate customer
    discounted_total = original_total * (1 - discount_rate) if is_corporate_customer else original_total
    discounted_total = round(discounted_total, 2)  
    print("discounted_total",discounted_total) 
    # Update the total in the order if a corporate discount is applied
    if is_corporate_customer:
        order.total = discounted_total
        db.session.commit()

    if request.method == 'POST':
        # Retrieve the necessary information from the form
        payment_method = request.form.get('payment_method')

        # Process payment based on method
        payment = None
        if payment_method == 'credit_card':
            card_number = request.form.get('card_number')
            expiry_date = request.form.get('expiry_date')
            card_type = request.form.get('card_type')
            
            # Check if payment record exists
            payment = CreditCardPayment.query.filter_by(customer_id=customer_id, id=order.id).first()
            if not payment:
                payment = CreditCardPayment(
                    amount=discounted_total,
                    customer_id=customer_id,
                    card_number=card_number,
                    card_type=card_type,
                    expiry_date=expiry_date,
                )
                db.session.add(payment)
            else:
                # Update existing payment if needed
                payment.amount = discounted_total
                payment.card_number = card_number
                payment.card_type = card_type
                payment.expiry_date = expiry_date

        elif payment_method == 'debit_card':
            bank_name = request.form.get('bank_name')
            card_number = request.form.get('card_number_debit')

            # Check if payment record exists
            payment = DebitCardPayment.query.filter_by(customer_id=customer_id, id=order.id).first()
            if not payment:
                payment = DebitCardPayment(
                    amount=discounted_total,
                    customer_id=customer_id,
                    bank_name=bank_name,
                    card_number=card_number,
                )
                db.session.add(payment)
            else:
                # Update existing payment if needed
                payment.amount = discounted_total
                payment.bank_name = bank_name
                payment.card_number = card_number

        # Finalize the order and payment
        if payment:
            db.session.commit()
            # Update order status to 'Paid'
            order.status = 'Paid'
            db.session.commit()

            flash("Payment processed successfully!")
            return redirect(url_for('products'))
        else:
            flash("Payment processing failed. Please try again.")
            return redirect(url_for('checkout'))
            
    return render_template('checkout.html', order=order, original_total=original_total, discounted_total=discounted_total, is_corporate_customer=is_corporate_customer)
