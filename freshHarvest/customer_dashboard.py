from flask import Flask, render_template, session, flash, redirect, url_for
from freshHarvest import app


@app.route('/customer_dashboard')
def customer_dashboard():
    if 'user' in session and session.get('role') in ['customer', 'corporate_customer']:
        # Customer-only content
        return render_template('customer_dashboard.html')
    else:
        flash("Unauthorized access.")
        return redirect(url_for('login'))