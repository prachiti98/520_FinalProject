from flask.templating import render_template
from flask import Blueprint,current_app
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from models.TransactionDAO import TransactionDAO


staff_analyse_book_blueprint = Blueprint('staff_analyse_book_blueprint', __name__)

# Creating the Books list
@staff_analyse_book_blueprint.route('/analyse', methods=['GET', 'POST'])
def staffAnalyset():
    DAO = current_app.config['dao']
    transaction = TransactionDAO(DAO)
    result,h = transaction.analyse_data()
    return render_template('analyse.html', data=result)



