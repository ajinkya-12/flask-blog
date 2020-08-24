from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1,64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password_conf',
        message='Password must match')])
    password_conf = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    #Custom validator for the field email to check if it already exists
    def validate_email(self, field):
        if User.query.filter_by(email = field.data).first():
            return ValidationError('Email already exists')
    
    #Custom validator for the field username to check if it already exists
    def validate_username(self, field):
        if User.query.filter_by(username = field.data).first():
            return ValidationError('Username already exists')
