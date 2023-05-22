from flask.templating import render_template
from flask import Blueprint,current_app
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, IntegerField
from functools import wraps
from models.BookDAO import BookDAO
from controllers.index import is_logged_in
import datetime
import time
from models.TransactionDAO import TransactionDAO
from models.StudentDAO import StudentDAO

staff_return_book_blueprint = Blueprint('staff_return_book_blueprint', __name__)

# Return books
class ReturnForm(Form):
    book_name = StringField("Name of the book to be returned")
    studentUsername = StringField(
        "Student ID number", [validators.Length(min=1)])

@staff_return_book_blueprint.route('/return_books', methods=['GET', 'POST'])
@is_logged_in
def return_books():
    #Getting various data access objects
    DAO = current_app.config['dao']
    book = BookDAO(DAO)
    transaction = TransactionDAO(DAO)
    student = StudentDAO(DAO)
    result,pass_flag  = book.unavailable_books()    
    form = ReturnForm(request.form)
    #Get all users to check later if present
    all_users = student.get_all_users()
    all_users = [item['studentUsername'] for item in all_users[0]]
    
    #Check if return is possible
    if pass_flag > 0:
        if request.method == 'POST' and form.validate():
            student_id = form.studentUsername.data
            #Check if user is present
            if student_id in all_users:
                book_name = form.book_name.data
                data,h = transaction.getBook(student_id,book_name)
                if h > 0:
                    book_id = data[0]['book_id']
                    #Set book as availble
                    book.set_availble(book_id)
                    #Complete transaction
                    transaction.update_transaction(student_id,book_id)
                    return_date,h = transaction.get_return_date(student_id,book_id)
                    data = return_date
                    returndate = str(data[0]['returnDate'])
                    current_time = time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime())
                    #Check if the current date is > return date. If it is then add fine.
                    if current_time > returndate:
                        returndate = time.strftime(returndate)
                        datetimeFormat = '%Y-%m-%d %H:%M:%S'
                        diff = datetime.datetime.strptime(current_time, datetimeFormat)\
                - datetime.datetime.strptime(returndate, datetimeFormat)
                        amount_to_be_added_to_fine = (diff.days)*10
                        #Update the fine
                        transaction.update_fine(student_id,amount_to_be_added_to_fine)
                    else:
                        returndate = time.strftime(returndate)
                        datetimeFormat = '%Y-%m-%d %H:%M:%S'
                        diff = datetime.datetime.strptime(current_time, datetimeFormat)\
                - datetime.datetime.strptime(returndate, datetimeFormat)
                    #Return the book after adding the fine
                    flash('Book Returned', 'success')
                    return redirect(url_for('staff_bookslist_blueprint.staffbookslist'))
                else:
                    flash('Book already returned', 'success')
                    return redirect(url_for('staff_bookslist_blueprint.staffbookslist'))
            else:
                error = 'Invalid username'
                return render_template('return_books.html', form=form, books=result, error = error)
    else:
        flash('No books found', 'success')
    return render_template('return_books.html', form=form, books=result)






        