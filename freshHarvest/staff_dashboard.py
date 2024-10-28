from flask import Flask, render_template, session, flash, redirect, url_for
from freshHarvest import app


@app.route('/staff_dashboard')
def staff_dashboard():
    if 'user' in session and session.get('role') == 'staff':
        # Staff-only content
        return render_template('staff_dashboard.html')
    else:
        flash("Unauthorized access.")
        return redirect(url_for('login'))

