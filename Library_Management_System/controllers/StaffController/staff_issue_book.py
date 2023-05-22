#Issue and return books
from flask.templating import render_template
from flask import Blueprint,current_app
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps
from models.BookDAO import BookDAO
from controllers.index import is_logged_in
from models.TransactionDAO import TransactionDAO
from models.StudentDAO import StudentDAO

staff_issue_book_blueprint = Blueprint('staff_issue_book_blueprint', __name__)

class IssueForm(Form):
    bookName = StringField("Name of the book to be issued")
    studentUsername = StringField("Student ID number", [validators.Length(min=1)])

@staff_issue_book_blueprint.route('/issue_books/<string:bookName>', methods=['GET', 'POST'])
@is_logged_in
def issue_books(bookName):
    DAO = current_app.config['dao']
    #Getting various data access objects
    book = BookDAO(DAO)
    student = StudentDAO(DAO)
    transaction = TransactionDAO(DAO)
    result,h = book.get_issue_book(bookName)
    form = IssueForm(request.form)
    form.bookName.data = bookName
    all_users = student.get_all_users()
    #Get all users to check later if present
    all_users = [item['studentUsername'] for item in all_users[0]]
    if request.method == 'POST' and form.validate():
        student_id = form.studentUsername.data
        #Check if user is present
        if student_id in all_users:
            bookName = form.bookName.data
            book.issue_book(result[0])
            transaction.issue_book(student_id,session['staffUsername'], bookName,result[0]['book_id'])
            flash('Book Issued', 'success')
            return redirect(url_for('staff_bookslist_blueprint.staffbookslist'))
        else:
            error = 'Invalid username'
            return render_template('issue_books.html', form=form, error = error)
    return render_template('issue_books.html', form=form)


