from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from passlib.hash import sha256_crypt
from functools import wraps
from flask import Blueprint,current_app
from models.StaffDAO import StaffDAO

staff_login_blueprint = Blueprint('staff_login_blueprint', __name__)

# User Login
@staff_login_blueprint.route('/staff_login', methods=['GET', 'POST'])
def stafflogin():
    if request.method == 'POST':
        DAO = current_app.config['dao']
        #Get form fields
        staffUsername = request.form['staffUsername']
        password = request.form['password']
        staff = StaffDAO(DAO)
        result,cur = staff.getUser(staffUsername)
        if result > 0:
            # Get the stored hash
            data = cur.fetchone()
            originalPassword = data['password']
            # Comparing the Passwords
            if sha256_crypt.verify(password, originalPassword):
                # Password matched
                session['logged_in'] = True
                session['staff_logged_in'] = True
                session['staffUsername'] = staffUsername
                # session['aadharNo'] = data['aadharNo']
                flash('You have successfully logged in', 'success')
                return redirect(url_for('staff_bookslist_blueprint.staffbookslist'))
            else:
                error = 'Invalid login.'
                return render_template('staff_login.html', error = error)
        else:
            error = 'Username not found.'
            return render_template('staff_login.html', error = error)
    return render_template('staff_login.html')
