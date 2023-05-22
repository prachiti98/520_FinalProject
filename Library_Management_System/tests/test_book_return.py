import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask.helpers import url_for
from flask import current_app
from models.BookDAO import BookDAO
from models.TransactionDAO import TransactionDAO
from models.StudentDAO import StudentDAO
from controllers.StaffController.staff_return_book import staff_return_book_blueprint, ReturnForm


def test_return_books(client: FlaskClient, app: Flask):
    with app.app_context():
        # Provide the necessary data for registration
        staff_data = {
            'staffName': 'John Doe',
            'staffUsername': 'johndoestaff457',
            'password': 'password123',
            'confirm': 'password123'
        }

        # Send a POST request to the staff registration route
        response = client.post("/staff_register", data=staff_data)

        # Provide the necessary data for registration
        staff_login_data = {
            'staffUsername': staff_data['staffUsername'],
            'password': staff_data['password']
        }


        # Send a POST request to the staff login route
        response = client.post("/staff_login", data=staff_login_data)

        #create test student account
        # Provide the necessary data for registration
        student_data = {
            'studentName': 'John Doe',
            'email': 'johndoe@example.com',
            'mobile': '011234567890',
            'studentUsername': 'johndoe_checkfine',
            'password': 'password123',
            'confirm': 'password123'
        }

        # Send a POST request to the student registration route
        response = client.post("/studentregister", data=student_data)

        # Provide the necessary data for book addition
        book_data = {
            'bookName': 'Test Book',
            'author': 'Test Author',
            'quantity': 5
        }

        # Send a POST request to the add_books route
        response = client.post("/add_books", data=book_data)
        # Create an instance of TransactionDAO
        book_dao = BookDAO(current_app.config['dao'])
        result,h = book_dao.get_issue_book(book_data['bookName'])
        transaction_dao = TransactionDAO(current_app.config['dao'])
        book = result[0]
        book_dao.issue_book(book)
        transaction_dao.issue_book(student_data['studentUsername'], staff_data['staffUsername'], book_data['bookName'],book['book_id'] )
       

        # Create an instance of TransactionDAO
        transaction_dao = TransactionDAO(current_app.config['dao'])

        result, h = book_dao.search_book(book_data['bookName'])
        old_book_count = result[0]['available']

        # Provide the necessary data for book return
        return_data = {
            'book_name': book_data['bookName'],
            'studentUsername': student_data['studentUsername']
        }

        # Send a POST request to the return_books route
        response = client.post("/return_books", data=return_data)

        # Assert the response status code
        assert response.status_code == 302


        result, h = book_dao.search_book(book_data['bookName'])
        new_book_count = result[0]['available']

        # Assert the book is set as available
        assert old_book_count + 1  == new_book_count

        
