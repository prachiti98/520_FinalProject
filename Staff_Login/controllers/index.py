from flask.templating import render_template
from flask import Blueprint
from functools import wraps
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request

index_blueprint = Blueprint('index_blueprint', __name__)


@index_blueprint.route("/")
def index():
    return render_template("home.html")

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, please Login.', 'danger')
            return redirect(url_for('login'))
    return wrap