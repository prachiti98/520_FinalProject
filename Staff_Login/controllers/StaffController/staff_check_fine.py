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

staff_check_fine_blueprint = Blueprint('staff_check_fine', __name__)

    
@staff_check_fine_blueprint.route('/check_fine', methods=['GET', 'POST'])
@is_logged_in
def check_fine():
    DAO = current_app.config['dao']
    transaction = TransactionDAO(DAO)
    result,h = transaction.get_all_fines()
    if h > 0:
        return render_template('check_fine.html', books=result)
    else:
        msg = 'No outstanding fines'
        return render_template('check_fine.html', msg=msg)


    



