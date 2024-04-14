from flask_wtf import FlaskForm
from wtforms.fields import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import data_required, length, email


class LoginForm(FlaskForm):
    first_name = StringField('First Name', validators=[data_required(), length(5, 50)],
                             render_kw={'placeholder': 'Enter First Name', 'class': 'form-control'})
    last_name = StringField('Last Name', validators=[data_required(), length(5, 50)],
                            render_kw={'placeholder': 'Enter Last Name', 'class': 'form-control'})
    email = EmailField('Email', validators=[data_required(), length(9, 80), email()])
    password = PasswordField('Password', validators=[data_required()])
    submit = SubmitField('Login')
