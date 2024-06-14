from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, \
    TextAreaField
from wtforms.validators import data_required, ValidationError


def validate_length(form, field):
    if 50 <= len(field.data) or len(field.data) < 5:
        raise ValidationError('Field Length Must Be in range (5, 50)')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[data_required()],
                        render_kw={'placeholder': 'შეიყვანეთ პოსტის სათაური', 'class': 'form-control'})
    content = TextAreaField('Title', validators=[data_required()],
                        render_kw={'placeholder': 'შეიყვანეთ პოსტის კონტენტი', 'class': 'form-control'})
    submit = SubmitField('Create Post', render_kw={'class': 'btn btn-primary', 'style': 'text-align: center;'})
