from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from website.models import User
from website import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #data = request.form
        
        email = request.form['email']
        password = request.form['password']
        # Process login logic here
        if len(email) < 3 or len(password) <5:
            flash("Email and Password cannot be empty or less than 5 characters", category='error')
        else:
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash("Logged in successfully!", category='success')
                return redirect(url_for('view_bp.home'))
            else:
                flash("Invalid email or password", category='error')
    return render_template("login.html", user=current_user)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        # Process signup logic here
        if len(email) < 3 or len(password) < 5:
            flash("Email and password cannot be empty", category='error')
        elif len(first_name) < 2 or len(last_name) < 2:
            flash("First and last names must be at least 2 characters", category='error')
        else:
            # Check if user already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash("Email already registered", category='error')
            else:
                # Use a supported password hashing method. Werkzeug expects methods like
                # 'pbkdf2:sha256', 'pbkdf2:sha512', 'bcrypt', etc. 'sha256' alone is invalid.
                new_user = User(email=email, first_name=first_name, password=generate_password_hash(password, method='pbkdf2:sha256'))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash("Account created successfully!", category='success')
                return redirect(url_for('view_bp.home'))

    return render_template("signup.html", user=current_user)

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", category='success')
    return redirect(url_for('auth.login'))
    
