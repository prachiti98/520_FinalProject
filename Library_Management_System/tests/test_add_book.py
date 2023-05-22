from flask import current_app
from models.StudentDAO import StudentDAO
from controllers.StudentController.student_register import student_register_blueprint, StudentRegisterForm
from flask import Flask
from flask.testing import FlaskClient
from flask.helpers import url_for
from flask import current_app
from models.BookDAO import BookDAO
from controllers.StaffController.staff_register import staff_register_blueprint, RegisterForm


def test_add_books(client: FlaskClient, app: Flask):
    with app.app_context():

        # Provide the necessary data for registration
        data = {
            'staffName': 'John Doe',
            'staffUsername': 'johndoestaff456',
            'password': 'password123',
            'confirm': 'password123'
        }

        # Send a POST request to the staff registration route
        response = client.post("/staff_register", data=data)

        # Provide the necessary data for registration
        staff_data = {
            'staffUsername': data['staffUsername'],
            'password': data['password']
        }


        # Send a POST request to the staff login route
        response = client.post("/staff_login", data=staff_data)

        # Create an instance of BookDAO
        dao = BookDAO(current_app.config['dao'])

        # Provide the necessary data for book addition
        data = {
            'bookName': 'Test Book',
            'author': 'Test Author',
            'quantity': 5
        }

        # Send a POST request to the add_books route
        response = client.post("/add_books", data=data)

        # Assert the response status code
        assert response.status_code == 302

        # Assert the flashed message
        with client.session_transaction() as session:
            flashed_messages = session.get('_flashes', [])
            assert len(flashed_messages) == 3
            assert flashed_messages[0][1] == 'You are now registered.'
            assert flashed_messages[1][1] == 'You have successfully logged in'
            assert flashed_messages[2][1] == 'Books Added'
            

        # Retrieve the added books from the database
        count, books = dao.getBooks()
        
        # Find the added book in the retrieved books
        added_book = next((book for book in books._rows if book['bookName'] == data['bookName']), None)
        
        # Assert the book is added successfully
        assert added_book is not None
        assert added_book['bookName'] == data['bookName']

        # Assert the redirected URL
        assert response.headers['Location'].endswith('/staffbookslist')

