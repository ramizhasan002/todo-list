from flask import Blueprint, render_template, redirect, url_for, flash
from sqlalchemy import or_
from flask_login import login_user, logout_user, login_required, current_user
from app.form import RegisterForm, LoginForm
from app.models import User
from app.extensions import db 

auth_bp = Blueprint("auth", __name__)

# Register Page 
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("tasks.home"))

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()

        if existing_user:
            flash("User already exists", "error")
            return redirect(url_for("auth.register"))
        
        if existing_email:
            flash("Email already registered", "error")
            return redirect(url_for("auth.register"))
        
        
        new_user = User(username=username, email=email, password=password)
        try:
            db.session.add(new_user)
            db.session.commit()

            flash("Account created! Please sign in.", "success")
            return redirect(url_for("auth.login"))
        
        except Exception:
            db.session.rollback()
            flash("Something went wrong. Please try again.", "error")
            return redirect(url_for("auth.register"))

    return render_template("register.html", form=form)

# Login Page
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("tasks.home"))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user_input = form.user_input.data
        password = form.password.data

        user = User.query.filter(
            or_(User.username == user_input,
                User.email == user_input)
        ).first()

        if user:
            if user.check_password(password):
                login_user(user, remember=True)
                flash("Login Successful", "success")
                return redirect(url_for("tasks.home"))
            else:
                flash("Wrong password", "error")
                return redirect(url_for("auth.login"))
        else:
            flash("User doesn't exists", "error")
            return redirect(url_for("auth.login"))

    return render_template("login.html", form=form)

# Logout 
@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for("auth.login"))
