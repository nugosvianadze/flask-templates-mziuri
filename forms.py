from flask_wtf import FlaskForm
from wtforms import FormField
from wtforms.fields import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import data_required, length, email, ValidationError


def validate_length(form, field):
    if 50 <= len(field.data) or len(field.data) < 5:
        raise ValidationError('Field Length Must Be in range (5, 50)')

class LoginForm(FlaskForm):
    first_name = StringField('First Name', validators=[data_required(), validate_length],
                             render_kw={'placeholder': 'შეიყვანეთ სახელი', 'class': 'form-control'})
    last_name = StringField('Last Name', validators=[data_required(), validate_length],
                            render_kw={'placeholder': 'შეიყვანეთ გვარი', 'class': 'form-control'})
    email = EmailField('Email', validators=[data_required(), length(9, 80), email()])
    password = PasswordField('Password', validators=[data_required()])
    submit = SubmitField('Login')

    # def validate_first_name(self, field):
    #     if 50 <= len(field.data) or len(field.data) < 5:
    #         raise ValidationError('Field Length Must Be in range (5, 50)')

    # def validate(self, extra_validators=None):
    #     print(self.data)
    #     return self.data

class ContactForm(FlaskForm):
    user = FormField(LoginForm)
