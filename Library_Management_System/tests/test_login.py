from flask import current_app
from models.StudentDAO import StudentDAO
from controllers.StudentController.student_login import student_login_blueprint
from flask import Flask
from flask.testing import FlaskClient
from flask import current_app
from werkzeug.datastructures import ImmutableMultiDict
from passlib.hash import sha256_crypt
from models.StaffDAO import StaffDAO
from flask import session

def test_student_login_valid(client, app):
    with app.app_context():
        # Create an instance of StudentDAO
        dao = StudentDAO(current_app.config['dao'])

        # Provide the necessary data for registration
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
        
        # Assert the response status code
        assert response.status_code == 302

        # Check if the session variables are set correctly
        with client.session_transaction() as session:
            assert session['logged_in']
            assert session['student_logged_in']
            assert session['studentUsername'] == data['studentUsername']

        # Assert the redirected URL
        assert response.headers['Location'].endswith('/studentbookslist')



def test_staff_login_valid(client: FlaskClient, app: Flask):
    with app.app_context():
        # Create an instance of StaffDAO
        dao = StaffDAO(current_app.config['dao'])

        # Provide the necessary data for registration
        data = {
            'staffName': 'John Doe',
            'staffUsername': 'johndoestaff123',
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

        # Assert the response status code
        assert response.status_code == 302

        # Check if the session variables are set correctly
        with client.session_transaction() as session:
            assert session['logged_in']
            assert session['staff_logged_in']
            assert session['staffUsername'] == staff_data['staffUsername']

        # Assert the flashed message
        with client.session_transaction() as session:
            flashed_messages = session['_flashes']
            assert len(flashed_messages) == 2  # Expecting 2 flashed messages

            # Check the content of each flashed message
            assert ('success', 'You are now registered.') in flashed_messages
            assert ('success', 'You have successfully logged in') in flashed_messages

        # Assert the redirected URL
        assert response.headers['Location'].endswith('/staffbookslist')


def test_staff_login_invalid_username(client: FlaskClient, app: Flask):
    with app.app_context():
        # Create an instance of StaffDAO
        dao = StaffDAO(current_app.config['dao'])

        # Provide the necessary data for registration
        data = {
            'staffName': 'John Doe',
            'staffUsername': 'johndoestaff123',
            'password': 'password123',
            'confirm': 'password123'
        }

        # Send a POST request to the staff registration route
        response = client.post("/staff_register", data=data)

        # Provide the necessary data for an invalid login
        invalid_data = {
            'staffUsername': 'johndoestaff123s',
            'password': 'invalidpassword'
        }

        # Send a POST request to the staff login route with invalid credentials
        response = client.post("/staff_login", data=invalid_data)

        # Assert the response status code
        assert response.status_code == 200

        # Assert there are no flashed messages
        with client.session_transaction() as session:
            flashed_messages = session.get('_flashes', [])
            assert len(flashed_messages) == 0

        # Assert the rendered template
        assert b'Username not found.' in response.data


def test_staff_login_invalid_password(client: FlaskClient, app: Flask):
    with app.app_context():
        # Create an instance of StaffDAO
        dao = StaffDAO(current_app.config['dao'])

        # Provide the necessary data for registration
        data = {
            'staffName': 'John Doe',
            'staffUsername': 'johndoestaff234',
            'password': 'password123',
            'confirm': 'password123'
        }

        # Send a POST request to the staff registration route
        response = client.post("/staff_register", data=data)

        # Provide the necessary data for an invalid login
        invalid_data = {
            'staffUsername': data['staffUsername'],
            'password': 'invalidpassword'
        }

        # Send a POST request to the staff login route with invalid credentials
        response = client.post("/staff_login", data=invalid_data)

        # Assert the response status code
        assert response.status_code == 200

        # Assert there are no flashed messages
        with client.session_transaction() as session:
            flashed_messages = session.get('_flashes', [])
            assert len(flashed_messages) == 0

        # Assert the rendered template
        assert b'Invalid login.' in response.data
