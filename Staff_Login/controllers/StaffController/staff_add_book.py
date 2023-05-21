from flask.templating import render_template
from flask import Blueprint,current_app
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, IntegerField
from passlib.hash import sha256_crypt
from functools import wraps
from models.BookDAO import BookDAO
from controllers.index import is_logged_in

staff_add_book_blueprint = Blueprint('staff_add_book_blueprint', __name__)

class AddBooksForm(Form):
    bookName = StringField("Name of the book to be added")
    author = StringField("Name of the Author")
    quantity = IntegerField("Enter the quantity to be added")

@staff_add_book_blueprint.route('/add_books', methods=['GET', 'POST'])
@is_logged_in
def add_books():
    DAO = current_app.config['dao']
    book = BookDAO(DAO)
    form = AddBooksForm(request.form)
    if request.method == 'POST' and form.validate():
        bookName = form.bookName.data
        author = form.author.data
        quantity = form.quantity.data
        while quantity:
            book.add_book(bookName,author)
            quantity-=1
        flash('Books Added', 'success')
        return redirect(url_for('staff_bookslist_blueprint.staffbookslist'))
    return render_template('add_books.html', form=form)
