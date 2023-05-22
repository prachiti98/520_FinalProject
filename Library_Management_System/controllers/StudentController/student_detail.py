from flask.templating import render_template
from flask import Blueprint,current_app
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from models.TransactionDAO import TransactionDAO
from controllers.StudentController.student_login import student_login_blueprint
from controllers.index import is_logged_in

student_detail_blueprint = Blueprint('student_detail_blueprint', __name__)

@student_detail_blueprint.route("/student_detail", methods=['GET', 'POST'])
@is_logged_in('student')
def student_detail():
    # Create Cursor
    # cur = mysql.connection.cursor()

    # # Execute
    # result = cur.execute("SELECT * FROM transactions WHERE studentUsername = %s", (session['studentUsername'], )) 
    DAO = current_app.config['dao']
    transaction = TransactionDAO(DAO)
    result,cur = transaction.getUser(session['studentUsername'])

    transactions = cur.fetchall()

    fine_result,cur = transaction.getFine(session['studentUsername'])
    # fine_result = cur.execute("select fine from transactions where studentUsername like %s",(session['studentUsername'], ))

    fine=cur.fetchone()
    
    if result > 0 and fine_result > 0:
        return render_template('student_detail.html', transactions = transactions,fine=fine['fine'])
    elif result > 0:
        return render_template('student_detail.html', transactions = transactions,fine=0)
    else:
        msg = 'No recorded transactions'
        return render_template('student_detail.html', msg= msg)

    # Close connection
    cur.close()