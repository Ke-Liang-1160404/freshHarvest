#import 
from flask import render_template, request, redirect, url_for, session,flash
from flask_hashing import Hashing
from freshHarvest import db, app

from freshHarvest.models import PeopleModels, ProductModels, OrderPaymentModels
from flask_hashing import Hashing

hashing= Hashing(app)
hashihng_salt="freshHarvest"

#login page
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.pop('user', None)
        
        username= request.form['username']
        password= request.form['password']
        hashed_password=hashing.hash_value(password,hashihng_salt)
        print(hashed_password)
        
        user= PeopleModels.Customer.query.filter_by(username=username).first_or_404()
        print("here")
        print("!!!!!!!",user)
        print("here")
        if user:
                is_valid= hashing.check_value(user.password,password,hashihng_salt)
                print("check_password is", is_valid)
                if is_valid:
                  session['user']= user.username
                  flash="login successfully"
                  print("login")
                  return redirect(url_for('index'))
                else:
                  print("not login")
                  return render_template('login.html', flash="something wrong")
        
        return redirect(url_for('login'))
    
    return render_template('login.html')
  
  
@app.route('/all_customers')
def all_customers():
  
    customers= PeopleModels.Customer.query.all()
    staff=PeopleModels.Staff.query.all()
    corporate=PeopleModels.CorporateCustomer.query.all()
    order=OrderPaymentModels.Order.query.all()
    payment=OrderPaymentModels.Payment.query.all()
    creditsCards= OrderPaymentModels.CreditCardPayment.query.all()
    debitCards=OrderPaymentModels.DebitCardPayment.query.all()
    item=ProductModels.Item.query.all()
    veggie=ProductModels.Veggie.query.all()
    box=ProductModels.PremadeBox.query.all()
    contents=ProductModels.PremadeBox.query.all()
    print(customers)
    print(staff,"/n",corporate,"/n",order,"/n",payment,"/n",creditsCards,"/n",debitCards,"/n",item,"/n",veggie,"/n",box,"/n",contents)
    return render_template('base.html', customers= customers)  