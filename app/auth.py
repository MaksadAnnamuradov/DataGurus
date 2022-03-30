from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth', __name__)
    
@auth.route('/login')
def login():
    return redirect(url_for('user.login'))


@auth.route('/signup')
def signup():
    return redirect(url_for('user.register'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.logout'))



