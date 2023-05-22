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


def test_student_detail_authenticated(client, app):
    with app.app_context():
        # Create an instance of StudentDAO
        dao = StudentDAO(current_app.config['dao'])

        # Provide the necessary data for registration
        student_data = {
            'studentName': 'John Doe 1',
            'email': 'johndoe1@example.com',
            'mobile': '011234567890',
            'studentUsername': 'johndoe238',
            'password': 'password123',
            'confirm': 'password123'
        }

        # Send a POST request to the student registration route
        response = client.post("/studentregister", data=student_data)
        
        # Assert the response status code
        assert response.status_code == 302
        # Provide the necessary data for login
        login_data = {
            'studentUsername': student_data['studentUsername'],
            'password': 'password123'
        }

        # Send a POST request to the student login route
        response = client.post("/studentlogin", data=login_data)
        
        response = client.get('/student_detail')
        assert b'Welcome' in response.data
        assert student_data['studentUsername'].encode('utf-8') in response.data