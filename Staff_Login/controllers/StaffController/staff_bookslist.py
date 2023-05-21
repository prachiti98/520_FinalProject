from flask.templating import render_template
from flask import Blueprint,current_app
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from models.BookDAO import BookDAO


staff_bookslist_blueprint = Blueprint('staff_bookslist_blueprint', __name__)

# Creating the Books list
@staff_bookslist_blueprint.route('/staffbookslist')
def staffbookslist():
    DAO = current_app.config['dao']
    book = BookDAO(DAO)
    result,cur = book.getStaffBooks()
    books = cur.fetchall()

    if result > 0:
        return render_template('staff_bookslist.html', books = books)
    else:
        msg = 'No books found'
        return render_template('staff_bookslist.html', msg= msg)