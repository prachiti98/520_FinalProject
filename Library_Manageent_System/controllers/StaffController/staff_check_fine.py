from flask.templating import render_template
from flask import Blueprint,current_app
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from functools import wraps
from controllers.index import is_logged_in
from models.TransactionDAO import TransactionDAO

staff_check_fine_blueprint = Blueprint('staff_check_fine', __name__)

    
@staff_check_fine_blueprint.route('/check_fine', methods=['GET', 'POST'])
@is_logged_in
def check_fine():
    #Getting Transaction data access object
    DAO = current_app.config['dao']
    transaction = TransactionDAO(DAO)
    #Get all the fines
    result,h = transaction.get_all_fines()
    #Use the results to render the template
    if h > 0:
        return render_template('check_fine.html', books=result)
    else:
        msg = 'No outstanding fines'
        return render_template('check_fine.html', msg=msg)


    



