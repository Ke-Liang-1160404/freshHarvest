from flask import Flask, render_template, request, redirect, url_for,jsonify
from freshHarvest import app, db
from freshHarvest.models import Users,users_schema,user_schema




@app.route('/')
def index():
    return render_template('adduser.html')



"""@app.route('/useradd',methods=['POST','GET'])
def useradd():
  if request.method == 'POST':
    name = request.form['name']
    email = request.form['email']

    name="kurt"
    email="kurtliang@gmail.com
 
    users = User(name,email)
    db.session.add(users)
    db.session.commit()
    return "<p>user added</p>"
    return models.user_schema.jsonify(users)
    
@app.route('/listusers',methods =['GET'])
def listusers():
    all_users = User.query.all()
    results = users_schema.dump(all_users)
    print("results",results)
    return render_template('alluser.html',users=results)"""
  
@app.route('/listusers',methods =['GET'])
def listusers():
    all_users = Users.query.all()
    results = users_schema.dump(all_users)
    return jsonify(results)
 
@app.route('/userdetails/<id>',methods =['GET'])
def userdetails(id):
    user = Users.query.get(id)
    return user_schema.jsonify(user)
 
@app.route('/userupdate/<id>',methods = ['PUT'])
def userupdate(id):
    user = Users.query.get(id)
 
    name = request.json['name']
    email = request.json['email']
 
    user.name = name
    user.email = email
 
    db.session.commit()
    return user_schema.jsonify(user)
 
@app.route('/userdelete/<id>',methods=['DELETE'])
def userdelete(id):
    user = Users.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)
 
@app.route('/useradd',methods=['POST'])
def useradd():
    name = request.json['name']
    email = request.json['email']
 
    users = Users(name,email)
    db.session.add(users)
    db.session.commit()
    return user_schema.jsonify(users)