from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from flask import Blueprint,current_app
from models.StaffDAO import StaffDAO
from controllers.StudentController.student_bookslist import student_bookslist_blueprint
from controllers.StaffController.staff_login import staff_login_blueprint
from models.StaffDAO import StaffDAO

class RegisterForm(Form):
    staffName = StringField("Name", [validators.Length(min=1, max=100)])
    staffUsername = StringField(
        'Staff Username', [validators.Length(min=1, max=100)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
        ])
    confirm = PasswordField('Confirm Password')


staff_register_blueprint = Blueprint('staff_register_blueprint', __name__)

# User register
@staff_register_blueprint.route('/staff_register', methods=['GET', 'POST'])
def staff_register():
        form = RegisterForm(request.form)
        DAO = current_app.config['dao']
        staff = StaffDAO(DAO)
        if request.method == 'POST' and form.validate():
            staffName = form.staffName.data
            staffUsername = form.staffUsername.data
            password = sha256_crypt.encrypt(str(form.password.data))
            staff.add_staff(staffName, staffUsername, password)
            flash("You are now registered.", 'success')
            return redirect(url_for('staff_login_blueprint.stafflogin'))
        return render_template('register.html', form=form)