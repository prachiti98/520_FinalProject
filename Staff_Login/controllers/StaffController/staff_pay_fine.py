from flask.templating import render_template
from flask import Blueprint,current_app
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from models.BookDAO import BookDAO
from controllers.index import is_logged_in
from models.TransactionDAO import TransactionDAO

staff_pay_fine_blueprint = Blueprint('staff_pay_fine', __name__)

class GetUsernameForm(Form):
    studentUsername = StringField(
        "Student ID number", [validators.Length(min=1)])
    amountpaid = StringField("Student ID number")

@staff_pay_fine_blueprint.route('/pay_fine', methods=['GET', 'POST'])
@is_logged_in
def pay_fine():
    form = GetUsernameForm(request.form)
    newfine = 0
    data = 0
    DAO = current_app.config['dao']
    transaction = TransactionDAO(DAO)
    if request.method == 'POST' and form.validate():
        student_id = form.studentUsername.data
        data,h = transaction.get_fine(student_id)
        amountpaid = form.amountpaid.data
        if amountpaid and int(data[0]['fine']) > 0:
            originalfine = int(data[0]['fine'])
            newfine = 0
            newfine = originalfine-int(amountpaid)
            transaction.update_fine(newfine,student_id)
            flash('Amount was paid', 'success')
    return render_template('pay_fine.html', form=form, data=data, newfine=newfine)


         
        


