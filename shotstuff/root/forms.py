from flask_wtf import FlaskForm
from wtforms import (
  StringField,
  PasswordField,
)
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    """Form for logging in a user."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    """Form for registering a new user."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
