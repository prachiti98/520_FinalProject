
from flask import Flask
from flask.testing import FlaskClient


def test_search_staff_valid(client: FlaskClient, app: Flask):
    with app.app_context():
        # Provide the necessary data for registration
        staff_data = {
            'staffName': 'John Doe',
            'staffUsername': 'johndoestaff567',
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


        # Provide the necessary data for book addition
        book_data = {
            'bookName': 'Test Book',
            'author': 'Test Author',
            'quantity': 5
        }

        # Send a POST request to the add_books route
        response = client.post("/add_books", data=book_data)

        response = client.post('/staff_search_book', data={'search': book_data['bookName']})
        assert response.status_code == 200
        assert b'Test Book' in response.data

def test_search_staff_invalid(client: FlaskClient, app: Flask):
    with app.app_context():
        # Provide the necessary data for registration
        staff_data = {
            'staffName': 'John Doe',
            'staffUsername': 'johndoestaff567',
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


        # Provide the necessary data for book addition
        book_data = {
            'bookName': 'Test Book',
            'author': 'Test Author',
            'quantity': 5
        }

        # Send a POST request to the add_books route
        response = client.post("/add_books", data=book_data)

        response = client.post('/staff_search_book', data={'search': 'invalid book name'})
        assert response.status_code == 200
        assert b'No books found' in response.data


def test_search_student_valid(client: FlaskClient, app: Flask):
    with app.app_context():
        data = {
            'studentName': 'John Doe 1',
            'email': 'johndoe1@example.com',
            'mobile': '011234567890',
            'studentUsername': 'johndoe234',
            'password': 'password123',
            'confirm': 'password123'
        }

        # Send a POST request to the student registration route
        response = client.post("/studentregister", data=data)
        
        # Assert the response status code
        assert response.status_code == 302
        # Provide the necessary data for login
        data = {
            'studentUsername': 'johndoe234',
            'password': 'password123'
        }

        # Send a POST request to the student login route
        response = client.post("/studentlogin", data=data)


        # Provide the necessary data for book addition
        book_data = {
            'bookName': 'Test Book',
            'author': 'Test Author',
            'quantity': 5
        }

        # Send a POST request to the add_books route
        response = client.post("/add_books", data=book_data)

        response = client.post('/student_search_book', data={'search': book_data['bookName']})
        assert response.status_code == 200
        assert b'Test Book' in response.data


def test_search_student_invalid(client: FlaskClient, app: Flask):
    with app.app_context():
        data = {
            'studentName': 'John Doe 1',
            'email': 'johndoe1@example.com',
            'mobile': '011234567890',
            'studentUsername': 'johndoe234',
            'password': 'password123',
            'confirm': 'password123'
        }

        # Send a POST request to the student registration route
        response = client.post("/studentregister", data=data)
        
        # Assert the response status code
        assert response.status_code == 302
        # Provide the necessary data for login
        data = {
            'studentUsername': 'johndoe234',
            'password': 'password123'
        }

        # Send a POST request to the student login route
        response = client.post("/studentlogin", data=data)


        # Provide the necessary data for book addition
        book_data = {
            'bookName': 'Test Book',
            'author': 'Test Author',
            'quantity': 5
        }

        # Send a POST request to the add_books route
        response = client.post("/add_books", data=book_data)

        response = client.post('/student_search_book', data={'search': 'invalid book name'})
        assert response.status_code == 200
        assert b'No books found' in response.data