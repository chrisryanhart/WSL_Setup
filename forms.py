from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length
from wtforms.fields.html5 import EmailField

class AddUserForm(FlaskForm):
    """Form to add new user"""

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])

class UserLoginForm(FlaskForm):
    """Login existing user"""
    username = StringField('Username',validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField('Password',validators=[InputRequired(), Length(min=6, max=55)])

class AddFeedbackForm(FlaskForm):

        title = StringField('Title',validators=[Length(max=100),InputRequired()])
        content = StringField('Content',validators=[InputRequired()])


class DeleteForm(FlaskForm):
    """Delete form left blank"""