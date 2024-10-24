from flask import Flask, render_template, request, redirect, url_for,jsonify
from freshHarvest import app, db




@app.route('/')
def index():
    return render_template('base.html')



