from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from functools import wraps
from models.DBDAO import DBDAO
from controllers.index import index_blueprint
from controllers.about import about_blueprint
from controllers.StudentController.student_login import student_login_blueprint
from controllers.StudentController.student_register import student_register_blueprint
from controllers.StudentController.student_bookslist import student_bookslist_blueprint
from controllers.StudentController.student_detail import student_detail_blueprint
from controllers.StaffController.staff_login import staff_login_blueprint
from controllers.StaffController.staff_register import staff_register_blueprint
from controllers.StaffController.staff_bookslist import staff_bookslist_blueprint
from controllers.StaffController.staff_add_book import staff_add_book_blueprint
from controllers.StaffController.staff_return_book import staff_return_book_blueprint
from controllers.StaffController.staff_issue_book import staff_issue_book_blueprint
from controllers.StaffController.staff_check_fine import staff_check_fine_blueprint
from controllers.StaffController.staff_pay_fine import staff_pay_fine_blueprint
from controllers.StaffController.staff_analyse_book import staff_analyse_book_blueprint

app = Flask(__name__)

DAO = DBDAO(app)

app.config['dao'] = DAO

#Registering Students
app.register_blueprint(index_blueprint)
app.register_blueprint(about_blueprint)
app.register_blueprint(student_login_blueprint)
app.register_blueprint(student_register_blueprint)
app.register_blueprint(student_bookslist_blueprint)
app.register_blueprint(student_detail_blueprint)
#Registering Staff
app.register_blueprint(staff_login_blueprint)
app.register_blueprint(staff_bookslist_blueprint)
app.register_blueprint(staff_add_book_blueprint)
app.register_blueprint(staff_return_book_blueprint)
app.register_blueprint(staff_issue_book_blueprint)
app.register_blueprint(staff_check_fine_blueprint)
app.register_blueprint(staff_pay_fine_blueprint)
app.register_blueprint(staff_analyse_book_blueprint)
app.register_blueprint(staff_register_blueprint)

# User Login
@app.route('/staff_login', methods=['GET', 'POST'])
def staff_login():
    return render_template('staff_login.html')

@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    return render_template('student_login.html')

# Check if user logged in
#use the one in controllers.index and remove from here
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, please Login.', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/staff_logout')
@is_logged_in
def staff_logout():
    session.clear()
    flash('You have logged out.', 'success')
    return redirect(url_for('staff_login'))

@app.route('/student_logout')
@is_logged_in
def student_logout():
    session.clear()
    flash('You have logged out.', 'success')
    return redirect(url_for('student_login'))

if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True,port=8080)
