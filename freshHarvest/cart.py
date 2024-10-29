from flask import session, redirect, url_for, request, flash, render_template
from freshHarvest import app, db
from freshHarvest.models import Veggie, WeightedVeggie, PackVeggie, UnitPriceVeggie, BunchVeggie, Order, OrderLine,Item


@app.route('/cart')
def cart():
    if 'user' not in session:
        flash("Please log in to view your cart.")
        return redirect(url_for('login'))
    elif session.get('role') == 'staff':
        flash("Staff members do not have a cart.")
        return redirect(url_for('staff_dashboard'))
    elif session.get('role') in ['customer', 'corporate_customer']:
        customer_id = session['user_id']
        order = Order.query.filter_by(customer_id=customer_id, status='Pending').first()

        if order:
            order_lines = (
            OrderLine.query
            .join(Item, OrderLine.item_id == Item.id)
            .join(Order, OrderLine.order_id == Order.id)     
            .add_columns(Item.name, Item.type)        
            .all()
        )
            print("order_lines",order_lines)  
            # Access and print each order line along with its associated item details
            for order_line, item_name,item_type in order_lines:
                print(order_line)
                print(f"Item name: {item_name}, Quantity: {order_line.quantity} ") 
        else:
            order_lines = []

        return render_template('cart.html', order_lines=order_lines, order=order)
      


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'user' not in session:
        flash("Please log in to add items to your cart.")
        return redirect(url_for('login'))

    veggie_id = request.form.get('veggie_id')
    quantity = int(request.form.get('quantity'))

    # Retrieve the veggie by ID to get its details
    veggie = Veggie.query.get(veggie_id)
    print("veggie",veggie)
    print(f"The veggie is of type: {veggie.__class__.__name__}")


    weighted_veggie = WeightedVeggie.query.get(veggie_id)
    if weighted_veggie:
        veggie_type = "WeightedVeggie"

        unit_type = 'kg'
    elif PackVeggie.query.get(veggie_id):
        veggie_type = "PackVeggie"

        unit_type = 'pack'
    elif UnitPriceVeggie.query.get(veggie_id):
        veggie_type = "UnitPriceVeggie"

        unit_type = 'unit'
    else:
        flash("Unknown veggie type.")
        return redirect(url_for('products'))

    # Create or update order
    print("unit_type",unit_type)
    print("session",session)
    customer_id = session['user_id']  # Assuming user session contains their ID
    order = Order.query.filter_by(customer_id=customer_id, status='Pending').first()
    
    # If there's no existing pending order, create a new one
    if not order:
        order = Order(customer_id=customer_id, staff_id=None)  # staff_id can be set to None or a valid ID
        db.session.add(order)
        db.session.commit()  # Commit to get the order ID

    # Create or update the order line
    order_line = OrderLine.query.filter_by(order_id=order.id, item_id=veggie_id).first()
    
    if order_line:
        order_line.quantity += quantity  # Update quantity if the item is already in the order
    else:
        order_line = OrderLine(order_id=order.id, item_id=veggie_id, quantity=quantity)
        db.session.add(order_line)

    db.session.commit()  # Save changes to the database

    flash(f"{quantity} {unit_type}(s) of {veggie.name} added to your cart!")
    return redirect(url_for('products'))