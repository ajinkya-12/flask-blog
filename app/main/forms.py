from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from flask_login import current_user
from ..models import User

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditProfileForm(FlaskForm):
    uname = StringField('Username', validators=[DataRequired(), Length(1,64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers, dots or underscores')])
    name = StringField('Name', validators=[Length(0,64)])
    location = StringField('Location', validators=[Length(0,64)])
    bio = TextAreaField('About me')
    submit = SubmitField('Apply')

    def validate_uname(self, field):
        if field.data != current_user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in user.')
