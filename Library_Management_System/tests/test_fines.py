from flask import Flask
from flask.testing import FlaskClient
from flask.wrappers import Response
from flask import current_app
from models.BookDAO import BookDAO
from models.TransactionDAO import TransactionDAO

def test_check_fine(client: FlaskClient, app: Flask):
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
       
        count, result =  transaction_dao.getFineWithTransactionId(student_data['studentUsername'])
        transaction = result._rows[-1]
        transaction_dao.update_fine(transaction['transaction_id'], 10)
        
        # Send a GET request to the check_fine route
        response: Response = client.get("/check_fine")

        # Assert that the response status code is 200 (OK)
        assert response.status_code == 200

        # Assert that the correct template is rendered
        assert b'Student Fines' in response.data

        # Assert that the mock result is present in the rendered template
        assert b'johndoe_checkfine' in response.data

        # Cleanup - Logout the staff member
        client.get("/staff_logout")




def test_pay_fine(client: FlaskClient, app: Flask):
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
       
        count, result =  transaction_dao.getFineWithTransactionId(student_data['studentUsername'])
        transaction = result._rows[-1]
        transaction_dao.update_fine(transaction['transaction_id'], 10)

        form_data = {
            'studentUsername': student_data['studentUsername'],
            'amountpaid': '10'
        }

        # Send a POST request to the pay_fine route
        response = client.post("/pay_fine", data=form_data)

        # Assert the response status code
        assert response.status_code == 200

        # Assert the flash message
        assert b'Amount was paid' in response.data


        


