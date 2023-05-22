from flask.templating import render_template
from flask import Blueprint,current_app
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from models.BookDAO import BookDAO
from controllers.index import is_logged_in


staff_search_book_blueprint = Blueprint('staff_search_book_blueprint', __name__)

# Creating the Books list
@staff_search_book_blueprint.route('/staff_search_book', methods=['POST'])
@is_logged_in('staff')
def search_book():
    DAO = current_app.config['dao']
    book = BookDAO(DAO)
    if request.method == 'POST':
        #Search for the book
        search_text = request.form['search']
        result,cur = book.search_book(search_text )
        #Display only the search results
        if cur > 0:
            return render_template('staff_bookslist.html', books = result)
        else:
            msg = 'No books found'
            return render_template('staff_bookslist.html', msg= msg)
    
