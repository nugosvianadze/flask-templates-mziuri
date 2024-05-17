from flask_wtf import FlaskForm
from wtforms import FormField
from wtforms.fields import StringField, EmailField, PasswordField, SubmitField, IntegerField
from wtforms.validators import data_required, length, email, ValidationError


def validate_length(form, field):
    if 50 <= len(field.data) or len(field.data) < 5:
        raise ValidationError('Field Length Must Be in range (5, 50)')

class LoginForm(FlaskForm):
    first_name = StringField('First Name', validators=[data_required()],
                             render_kw={'placeholder': 'შეიყვანეთ სახელი', 'class': 'form-control'})
    last_name = StringField('Last Name', validators=[data_required()],
                            render_kw={'placeholder': 'შეიყვანეთ გვარი', 'class': 'form-control'})
    email = EmailField('Email', validators=[data_required(), length(9, 80), email()],
                       render_kw={'placeholder': 'შეიყვანეთ ემეილი', 'class': 'form-control'})
    password = PasswordField('Password', validators=[data_required()],
                             render_kw={'class': 'form-control', 'placeholder': 'შეიყვანეთ პაროლი'})
    submit = SubmitField('Login', render_kw={'class': 'btn btn-primary', 'style': 'text-align: center;'})

    # def validate_first_name(self, field):
    #     if 50 <= len(field.data) or len(field.data) < 5:
    #         raise ValidationError('Field Length Must Be in range (5, 50)')

    # def validate(self, extra_validators=None):
    #     print(self.data)
    #     return self.data


class ContactForm(FlaskForm):
    user = FormField(LoginForm)


class RegistrationForm(LoginForm):
    age = IntegerField('Age', validators=[data_required()], render_kw={'class': 'form-control',
    'placeholder': 'შეიყვანეთ ასაკი'})


class UserUpdateForm(RegistrationForm):
    email = None
    password = None
