from flask.templating import render_template
from flask import Blueprint,current_app
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from models.StudentDAO import StudentDAO
from controllers.StudentController.student_login import student_login_blueprint

student_register_blueprint = Blueprint('student_register_blueprint', __name__)

def validate_email(form, field):
    email = field.data
    if '@' not in email:
        raise validators.ValidationError('Invalid email address')
    
# Register Form Class
class StudentRegisterForm(Form):
    studentName = StringField("Student Name", [validators.Length(min=1, max=100)])
    studentUsername = StringField('Student Username', [validators.Length(min=1, max=25)])
    email = StringField('Email', validators=[validate_email])
    mobile = StringField("Mobile Number", [validators.Length(min=12, max=12)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
        ])
    confirm = PasswordField('Confirm Password')

@student_register_blueprint.route("/studentregister", methods=['GET', 'POST'])
#User Registration
def studentregister():
        DAO = current_app.config['dao']
        form = StudentRegisterForm(request.form)
        if request.method == 'POST' and form.validate():
            studentName = form.studentName.data
            email = form.email.data
            mobile = form.mobile.data
            studentUsername = form.studentUsername.data
            password = sha256_crypt.hash(str(form.password.data))
            student = StudentDAO(DAO)
            result = 0
            try:
                cur = student.addStudent(studentName,email,mobile,studentUsername,password)
                result = 1
            except:
                 pass
            if result>0:
                flash("You are now registered.", 'success')
            else:
                flash("Username already present. Use a different Username.", 'danger')

            return redirect(url_for('student_login_blueprint.studentlogin'))

        return render_template('student_register.html', form= form )