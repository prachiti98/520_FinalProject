from flask import current_app
from models.StudentDAO import StudentDAO
from controllers.StudentController.student_register import student_register_blueprint, StudentRegisterForm
from flask import Flask
from flask.testing import FlaskClient
from flask.helpers import url_for
from flask import current_app
from models.StaffDAO import StaffDAO
from controllers.StaffController.staff_register import staff_register_blueprint, RegisterForm

def test_student_register(client, app):
    with app.app_context():
        # Create an instance of StudentDAO
        dao = StudentDAO(current_app.config['dao'])

        # Provide the necessary data for registration
        data = {
            'studentName': 'John Doe',
            'email': 'johndoe@example.com',
            'mobile': '011234567890',
            'studentUsername': 'johndoe123',
            'password': 'password123',
            'confirm': 'password123'
        }

        # Send a POST request to the student registration route
        response = client.post("/studentregister", data=data)
        
        # Assert the response status code
        assert response.status_code == 302

        # Retrieve the registered student from the database
        count, h = dao.getUser(data['studentUsername'])
        assert h is not None
        
        registered_student = h._rows[0]
        assert registered_student is not None
        assert registered_student['studentName'] == data['studentName']
        assert registered_student['email'] == data['email']
        assert registered_student['mobile'] == data['mobile']
        assert registered_student['studentUsername'] == data['studentUsername']
        
        # Assert the redirected URL
        assert response.headers['Location'].endswith('/studentlogin')
        



def test_staff_register(client: FlaskClient, app: Flask):
    with app.app_context():
        # Create an instance of StaffDAO
        dao = StaffDAO(current_app.config['dao'])

        # Provide the necessary data for registration
        data = {
            'staffName': 'John Doe',
            'staffUsername': 'johndoe123',
            'password': 'password123',
            'confirm': 'password123'
        }

        # Send a POST request to the staff registration route
        response = client.post("/staff_register", data=data)

        # Assert the response status code
        assert response.status_code == 302

        # Retrieve the registered staff from the database
        count, h = dao.getUser(data['staffUsername'])
        assert h is not None
        registered_staff = h._rows[0]
        assert registered_staff is not None
        assert registered_staff['staffName'] == data['staffName']
        assert registered_staff['staffUsername'] == data['staffUsername']

        # Assert the flashed message
        with client.session_transaction() as session:
            flashed_messages = session['_flashes']
            assert len(flashed_messages) == 1
            assert flashed_messages[0][0] == 'success'
            assert flashed_messages[0][1] == 'You are now registered.'

        # Assert the redirection
        assert response.headers['Location'].endswith('/staff_login')