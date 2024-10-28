from flask import Flask, render_template, session, flash, redirect, url_for
from freshHarvest import app

from freshHarvest.models import ProductModels


@app.route('/products')
def products():
    if 'user' in session:

         # Retrieve all veggie types
        weighted_veggies = ProductModels.WeightedVeggie.query.all()
        pack_veggies = ProductModels.PackVeggie.query.all()
        unit_price_veggies = ProductModels.UnitPriceVeggie.query.all()
        bunch_veggies = ProductModels.BunchVeggie.query.all()
        
        # Create a dictionary for products to contain all veggie types
        products = {
            'weighted_veggies': weighted_veggies,
            'pack_veggies': pack_veggies,
            'unit_price_veggies': unit_price_veggies,
            'bunch_veggies': bunch_veggies
        }
        

        return render_template('products.html', products=products)  
    else:
        flash("Unauthorized access.")
        return redirect(url_for('login'))