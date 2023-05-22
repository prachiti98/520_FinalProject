from flask.templating import render_template
from flask import Blueprint,current_app
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from functools import wraps
from models.BookDAO import BookDAO


staff_bookslist_blueprint = Blueprint('staff_bookslist_blueprint', __name__)

# Creating the Books list
@staff_bookslist_blueprint.route('/staffbookslist')
def staffbookslist():
    #Getting Book data access object
    DAO = current_app.config['dao']
    book = BookDAO(DAO)
    #Get all the book
    result,cur = book.getStaffBooks()
    books = cur.fetchall()
    #Use the results to render the template
    if result > 0:
        return render_template('staff_bookslist.html', books = books)
    else:
        msg = 'No books found'
        return render_template('staff_bookslist.html', msg= msg)