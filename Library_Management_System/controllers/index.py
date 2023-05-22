from flask.templating import render_template
from flask import Blueprint
from functools import wraps
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request

index_blueprint = Blueprint('index_blueprint', __name__)


@index_blueprint.route("/")
def index():
    return render_template("home.html")

# Check if user logged in
def is_logged_in(role):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if 'logged_in' in session and session['role'] == role:
                return f(*args, **kwargs)
            else:
                flash(f'You need to login as a {role}', 'danger')
                return redirect(url_for(f'{role}_login'))
        return wrapped
    return decorator