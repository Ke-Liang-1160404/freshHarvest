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
        print("order",order)
        if order:
            order_lines = (
                OrderLine.query
                .join(Item, OrderLine.item_id == Item.id)
                .add_columns(Item.name, Item.type, Item.price)
                .filter(OrderLine.order_id == order.id)
                .all()
            )
            # Iterate through order_lines to see the results
            print(order_lines)
            for order_lien, line_item_name,line_item_type, line_item_price in order_lines:
              print(f"Item Name: {line_item_name}, Item Type: {line_item_type}, "
                f"Item Price: {line_item_price}"
                f"{order_lien}")
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
    elif BunchVeggie.query.get(veggie_id):
        veggie_type="BunchVeggie"
        unit_type="Buch"
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
        order = Order(customer_id=customer_id)  # staff_id can be set to None or a valid ID
        db.session.add(order)
        db.session.commit()  # Commit to get the order ID

    # Create or update the order line
    order_line = OrderLine.query.filter_by(order_id=order.id, item_id=veggie_id).first()
   
    if order_line:
        order_line.quantity += quantity  # Update quantity if the item is already in the order
        
    else:
        order_line = OrderLine(order_id=order.id, item_id=veggie_id, quantity=quantity)
      
        
        db.session.add(order_line)
        
    # Update the total price of the order
    order.total = order.order_total()
    
    
    db.session.commit()  # Save changes to the database

    flash(f"{quantity} {unit_type}(s) of {veggie.name} added to your cart!")
    return redirect(url_for('products'))
  
  
@app.route('/update_cart', methods=['POST'])
def update_cart():
    if 'user' not in session:
        flash("Please log in to update items in your cart.")
        return redirect(url_for('login'))

    order_item_id = request.form.get('order_item_id')
    quantity = int(request.form.get('quantity'))

    order_line = OrderLine.query.get(order_item_id)
    if order_line:
        if quantity > 0:
            order_line.quantity = quantity
            flash("Cart updated successfully!")
        else:
            flash("Quantity must be greater than zero.")
    else:
        flash("Item not found in cart.")
    # Update the total price of the order
    order = Order.query.get(order_line.order_id)
    order.total = order.order_total()
    db.session.commit()
    return redirect(url_for('cart'))


@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    if 'user' not in session:
        flash("Please log in to remove items from your cart.")
        return redirect(url_for('login'))

    order_item_id = request.form.get('order_item_id')

    order_line = OrderLine.query.get(order_item_id)
    if order_line:
        db.session.delete(order_line)
         # Update the total price of the order
        order = Order.query.get(order_line.order_id)
        order.total = order.order_total()

        db.session.commit()
        flash("Item removed from cart!")
    else:
        flash("Item not found in cart.")
        
   
    return redirect(url_for('cart'))
