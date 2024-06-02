from flask_wtf import FlaskForm
from wtforms import FormField
from wtforms.fields import StringField, EmailField, PasswordField, SubmitField, \
    IntegerField, TextAreaField, SelectMultipleField, FileField
from wtforms.validators import data_required, length, email, ValidationError
from flask_wtf.file import FileRequired, FileAllowed

from enums import RoleEnum

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
    address = StringField('Address', validators=[data_required()],
                          render_kw={'placeholder': 'შეიყვანეთ მისამართ', 'class': 'form-control'})
    roles = SelectMultipleField('Roles', choices=[(role.value, role.name) for role in RoleEnum])
    submit = SubmitField('Registration', render_kw={'class': 'btn btn-primary', 'style': 'text-align: center;'})
    profile_picture = FileField('Profile Picture',
                                validators=[FileAllowed(['jpg', 'png', 'svg', 'jpeg'])])


class UserUpdateForm(RegistrationForm):
    email = None
    password = None


class PostForm(FlaskForm):
    title = StringField('Title', validators=[data_required()],
                        render_kw={'placeholder': 'შეიყვანეთ პოსტის სათაური', 'class': 'form-control'})
    content = TextAreaField('Title', validators=[data_required()],
                        render_kw={'placeholder': 'შეიყვანეთ პოსტის კონტენტი', 'class': 'form-control'})
    submit = SubmitField('Create Post', render_kw={'class': 'btn btn-primary', 'style': 'text-align: center;'})