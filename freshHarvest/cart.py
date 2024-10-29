from flask import session, redirect, url_for, request, flash
from freshHarvest import app
from freshHarvest.models import Veggie, WeightedVeggie, PackVeggie, UnitPriceVeggie, BunchVeggie

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

    try:
        veggie = Veggie.query.get(veggie_id)
        
        if veggie is None:
            raise ValueError("Veggie not found.")
        
        # Attempt to identify the type of veggie
        try:
            weighted_veggie = WeightedVeggie.query.get(veggie_id)
            if weighted_veggie:
                price = weighted_veggie.price_per_kilo
                unit_type = 'kg'
                veggie_type = "WeightedVeggie"
        except Exception:
            weighted_veggie = None
        
        try:
            pack_veggie = PackVeggie.query.get(veggie_id)
            if pack_veggie:
                price = pack_veggie.price_per_pack
                unit_type = 'pack'
                veggie_type = "PackVeggie"
        except Exception:
            pack_veggie = None

        try:
            unit_price_veggie = UnitPriceVeggie.query.get(veggie_id)
            if unit_price_veggie:
                price = unit_price_veggie.price_per_unit
                unit_type = 'unit'
                veggie_type = "UnitPriceVeggie"
        except Exception:
            unit_price_veggie = None

        # If none of the subclass types matched, raise an error
        if not any([weighted_veggie, pack_veggie, unit_price_veggie]):
            raise ValueError("Unknown veggie type.")

    except ValueError as e:
        flash(str(e))
        return redirect(url_for('products'))


    # Prepare cart item details
    cart_item = {
        'name': veggie.name,
        'quantity': quantity,
        'price': price,
        'unit_type': unit_type
    }

    # Initialize cart in session if it doesn't exist
    if 'cart' not in session:
        session['cart'] = {}

    # Add or update item in cart
    if veggie_id in session['cart']:
        session['cart'][veggie_id]['quantity'] += quantity
    else:
        session['cart'][veggie_id] = cart_item

    flash(f"{quantity} {unit_type}(s) of {veggie.name} added to your cart!")
    return redirect(url_for('products'))
