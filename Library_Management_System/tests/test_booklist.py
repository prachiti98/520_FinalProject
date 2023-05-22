from flask import current_app
from models.StudentDAO import StudentDAO
from controllers.StudentController.student_register import student_register_blueprint, StudentRegisterForm
from flask import Flask
from flask.testing import FlaskClient
from flask.helpers import url_for
from flask import current_app
from models.BookDAO import BookDAO
from controllers.StaffController.staff_register import staff_register_blueprint, RegisterForm


def test_staffbookslist(client: FlaskClient, app: Flask):
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

        # Create an instance of BookDAO
        dao = BookDAO(current_app.config['dao'])

        # Mock the data returned by the getStaffBooks method
        mock_result = 2
        

        # Send a GET request to the staffbookslist route
        response = client.get("/staffbookslist")

        # Assert that the response status code is 200 (OK)
        assert response.status_code == 200
        
        assert b'Books List' in response.data
        assert b'Test Book' in response.data
        