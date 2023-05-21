#Issue and return books
from flask.templating import render_template
from flask import Blueprint,current_app
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from models.BookDAO import BookDAO
from controllers.index import is_logged_in

staff_issue_book_blueprint = Blueprint('staff_issue_book_blueprint', __name__)

class IssueForm(Form):
    bookName = StringField("Name of the book to be issued")
    studentUsername = StringField(
        "Student ID number", [validators.Length(min=1)])
    staffUsername = StringField('Enter your ID to authenticate', [
                                validators.Length(min=1)])
    

@staff_issue_book_blueprint.route('/issue_books/<string:bookName>', methods=['GET', 'POST'])
@is_logged_in
def issue_books(bookName):
    DAO = current_app.config['dao']
    book = BookDAO(DAO)
    result,h = book.get_issue_book(bookName)
    form = IssueForm(request.form)
    form.bookName.data = bookName
    if request.method == 'POST' and form.validate():
        student_id = form.studentUsername.data
        staff_id = form.staffUsername.data
        bookName = form.bookName.data
        book.issue_book(result)
        flash('Book Issued', 'success')
        return redirect(url_for('staff_bookslist_blueprint.staffbookslist'))
    return render_template('issue_books.html', form=form)


