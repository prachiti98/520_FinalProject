from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from flask import Blueprint,current_app
from models.StudentDAO import StudentDAO
from controllers.StaffController.staff_bookslist import staff_bookslist_blueprint

student_login_blueprint = Blueprint('student_login_blueprint', __name__)

# User Login
@student_login_blueprint.route('/studentlogin', methods=['GET', 'POST'])
def studentlogin():
    if request.method == 'POST':
        DAO = current_app.config['dao']
        #Get form fields
        studentUsername = request.form['studentUsername']
        password = request.form['password']

        student = StudentDAO(DAO)
        result,cur = student.getUser(studentUsername)

        if result > 0:

            # Get the stored hash
            data = cur.fetchone()
            originalPassword = data['password']


            # Comparing the Passwords
            if sha256_crypt.verify(password, originalPassword):

                # Password matched
                session['logged_in'] = True
                session['student_logged_in'] = True
                session['studentUsername'] = studentUsername
                # session['aadharNo'] = data['aadharNo']
                
                flash('You have successfully logged in', 'success')
                return redirect(url_for('student_bookslist_blueprint.studentbookslist'))

            else:
                error = 'Invalid login.'
                return render_template('student_login.html', error = error)

            #Close connection
            cur.close()

        else:
            error = 'Username not found.'
            return render_template('student_login.html', error = error)

    return render_template('student_login.html')
