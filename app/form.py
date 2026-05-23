from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo, ValidationError


def strong_password(form, field):
    val = field.data
    if not any(c.isupper() for c in val):
        raise ValidationError("Must contain at least one uppercase letter")
    if not any(c.isdigit() for c in val):
        raise ValidationError("Must contain at least one number")

class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(message="Username can't be empty"), 
            Regexp(r"^[A-Za-z0-9_.]+$", message="Only letters, '_' and '.' allowed")
            ]
        )

    email = StringField(
        "Email", 
        validators=[
            DataRequired(message="Email can't be empty"), 
            Email(message="Please enter a valid email")
            ]
        )

    password = PasswordField(
        "Password", 
        validators=[
            DataRequired(message="Password can't be empty"), 
            Length(min=8, message="Minimum 8 characters"), 
            Regexp(r"^[A-Za-z0-9_@]+$", message="Only letters, numbers, '_' and '@' allowed"),
            strong_password
            ]
        ) 

    confirm_password = PasswordField(
        "Confirm Password", 
        validators=[
            DataRequired(message="Please confirm your password"), 
            EqualTo("password", message="Passwords didn't match")
            ]
        )

    submit = SubmitField("Create account")


class LoginForm(FlaskForm):
    user_input = StringField(
        "Username or Email", 
        validators=[
            DataRequired(message="Please enter your username or email")
            ]
        )
    
    password = PasswordField(
        "Password", 
        validators=[
            DataRequired(message="Password can't be empty"), 
            ]
        ) 
    
    submit = SubmitField("Log in")


class EmptyForm(FlaskForm):
    pass


