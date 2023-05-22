from flask.templating import render_template
from flask import Blueprint,current_app
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from functools import wraps
from models.TransactionDAO import TransactionDAO


staff_analyse_book_blueprint = Blueprint('staff_analyse_book_blueprint', __name__)

@staff_analyse_book_blueprint.route('/analyse', methods=['GET', 'POST'])
def staffAnalyset():
    DAO = current_app.config['dao']
    #Getting the transaction data access object
    transaction = TransactionDAO(DAO)
    #Getting the data for analysis
    result,h = transaction.analyse_data()
    return render_template('analyse.html', data=result)


