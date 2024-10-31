from flask import Flask, render_template, session, flash, redirect, url_for, request, jsonify
from freshHarvest import app, db

from freshHarvest.models import ProductModels


@app.route('/products')
def products():
    if 'user' in session:

         # Retrieve all veggie types
        weighted_veggies = ProductModels.WeightedVeggie.query.all()
        pack_veggies = ProductModels.PackVeggie.query.all()
        unit_price_veggies = ProductModels.UnitPriceVeggie.query.all()
        bunch_veggies = ProductModels.BunchVeggie.query.all()
        premade_boxes = ProductModels.PremadeBox.query.all()  
        print( weighted_veggies, pack_veggies,unit_price_veggies,bunch_veggies
        )
        boxes=premade_boxes 
        # Create a dictionary for products to contain all veggie types
        products = {
            'weighted_veggies': weighted_veggies,
            'pack_veggies': pack_veggies,
            'unit_price_veggies': unit_price_veggies,
            'bunch_veggies': bunch_veggies
        }
        

        return render_template('products.html', products=products ,boxes=boxes)  
    else:
        flash("Unauthorized access.")
        return redirect(url_for('login'))
      
      
@app.route('/choose_box', methods=['GET', 'POST'])
def choose_box():
    if 'user' in session:
        if request.method == 'GET':
            # Retrieve available premade boxes and veggies
            boxes = ProductModels.PremadeBox.query.all()
            products = {
                'weighted': ProductModels.WeightedVeggie.query.all(),
                'pack': ProductModels.PackVeggie.query.all(),
                'unit_price': ProductModels.UnitPriceVeggie.query.all(),
                'bunch': ProductModels.BunchVeggie.query.all()
            }

            return render_template('choose_box.html', boxes=boxes, veggies=products)
        
        elif request.method == 'POST':
            box_id = request.form['box_id']
            veggie_selections = request.json.get('veggie_selections', [])
            
            # Retrieve the selected box and calculate space usage
            selected_box = ProductModels.PremadeBox.query.get(box_id)
            if not selected_box:
                return jsonify({"error": "Box not found"}), 404

            total_space_used = sum(veggie['space_occupied'] * veggie['quantity'] for veggie in veggie_selections)
            if total_space_used > selected_box.space:
                return jsonify({"error": "Space exceeded"}), 400

            # Save veggie selections to the box
            for veggie in veggie_selections:
                box_content = ProductModels.BoxContent(
                    box_id=selected_box.id,
                    veggie_id=veggie['id'],
                    quantity=veggie['quantity']
                )
                db.session.add(box_content)

            db.session.commit()
            flash("Items added to box successfully!")
            return jsonify({"success": "Items added successfully"}), 200
    
    else:
        flash("Unauthorized access.")
        return redirect(url_for('login'))