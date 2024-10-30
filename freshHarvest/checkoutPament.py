from flask import render_template, request, redirect, url_for, flash,session
from freshHarvest import db, app
from freshHarvest.models import Order, Payment, CreditCardPayment, DebitCardPayment
from datetime import datetime

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Retrieve the necessary information from the form
        payment_method = request.form.get('payment_method')
        customer_id = session['user_id']
        print("customer_id",customer_id)
        # Retrieve the pending order for the customer
        order = Order.query.filter_by(customer_id=customer_id, status='Pending').first()

        if not order:
            flash("No pending order found.")
            return redirect(url_for('products'))

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
                    amount=order.order_total(),
                    customer_id=customer_id,
                    card_number=card_number,
                    card_type=card_type,
                    expiry_date=expiry_date
                )
                db.session.add(payment)
            else:
                # Update existing payment if needed
                payment.amount = order.order_total()
                payment.card_number = card_number
                payment.card_type = card_type
                payment.expiry_date = expiry_date

        elif payment_method == 'debit_card':
            bank_name = request.form.get('bank_name')
            card_number = request.form.get('card_number_debit')
            print("card_number",card_number)
            
            # Check if payment record exists
            payment = DebitCardPayment.query.filter_by(customer_id=customer_id, id=order.id).first()
            if not payment:
                payment = DebitCardPayment(
                    amount=order.order_total(),
                    customer_id=customer_id,
                    bank_name=bank_name,
                    card_number=card_number
                )
                db.session.add(payment)
            else:
                # Update existing payment if needed
                payment.amount = order.order_total()
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
            
    return render_template('checkout.html')
