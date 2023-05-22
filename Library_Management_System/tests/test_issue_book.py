from flask import current_app
from models.TransactionDAO import TransactionDAO
from flask import Flask
from flask.testing import FlaskClient
from flask import current_app
from models.BookDAO import BookDAO


def test_book_issue(client: FlaskClient, app: Flask):
    with app.app_context():
        # Provide the necessary data for registration
        staff_data = {
            'staffName': 'John Doe',
            'staffUsername': 'johndoestaff459',
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
            'studentUsername': 'johndoe_issue_book',
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
        transaction_dao = TransactionDAO(current_app.config['dao'])
        
        result, h = book_dao.search_book(book_data['bookName'])
        old_book_count = result[0]['available']

        result,h = book_dao.get_issue_book(book_data['bookName'])
        book = result[0]
        book_dao.issue_book(book)
        transaction_dao.issue_book(student_data['studentUsername'], staff_data['staffUsername'], book_data['bookName'],book['book_id'] )
       



        result, h = book_dao.search_book(book_data['bookName'])
        new_book_count = result[0]['available']

        # Assert the book is set as available
        assert old_book_count == new_book_count + 1
