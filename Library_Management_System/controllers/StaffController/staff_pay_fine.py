from flask.templating import render_template
from flask import Blueprint,current_app
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps
from controllers.index import is_logged_in
from models.TransactionDAO import TransactionDAO

staff_pay_fine_blueprint = Blueprint('staff_pay_fine', __name__)

class GetUsernameForm(Form):
    studentUsername = StringField("Student Username", [validators.Length(min=1)])
    amountpaid = StringField("Username")

@staff_pay_fine_blueprint.route('/pay_fine', methods=['GET', 'POST'])
@is_logged_in('staff')
def pay_fine():
    form = GetUsernameForm(request.form)
    total_paid = 0
    data = 0
    fee_exist = 0
    amountpaid  = 0
    #Getting Transaction data access object
    DAO = current_app.config['dao']
    transaction = TransactionDAO(DAO)
    if request.method == 'POST' and form.validate():
        student_id = form.studentUsername.data
        #Getting total fine
        data,h = transaction.get_fine(student_id)
        #Getting amount paid
        amountpaid = int(form.amountpaid.data)
        total_paid = amountpaid
        transaction_data,h = transaction.get_fine_transactions(student_id)
        #Reduce the fine for each transaction based on the amount paid
        for t in transaction_data:
            fee_exist = 1
            if amountpaid:
                if amountpaid>t['fine']:
                    transaction.update_fine(t['transaction_id'],0)
                    amountpaid-=t['fine']
                else:
                    transaction.update_fine(t['transaction_id'],t['fine']-amountpaid)
                    amountpaid=0
        #Based on fine, display if there is any existing fine or not
        if fee_exist:
            flash('Amount was paid', 'success')
        else:
            flash('No accumulated fee', 'success')
    if amountpaid:
        return render_template('pay_fine.html', form=form, data=data, newfine=data[0]['fine'])
    else:
        return render_template('pay_fine.html', form=form, data=data, newfine=total_paid)


         
        


