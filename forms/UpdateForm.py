from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, IntegerField, SelectField, SubmitField, HiddenField
from wtforms.validators import Length, DataRequired, ValidationError

from models.book import book_list


def unique_title(form, field):
    for book in book_list:
        if book.id == int(form.id.data):
            continue
        if book.title == field.data and current_user.id == book.user_id:
            raise ValidationError('This title already exist', 422)

    return True


def unique_isbn(form, field) -> bool:
    for book in book_list:
        if book.id == int(form.id.data):
            continue
        if book.isbn == field.data and current_user.id == book.user_id:
            raise ValidationError('This ISBN already exist', 422)

    return True


class UpdateForm(FlaskForm):
    id = HiddenField('id')
    title = StringField('Title', validators=[DataRequired(), Length(min=3), unique_title])
    isbn = StringField('ISBN', validators=[DataRequired(), unique_isbn])
    category = SelectField('Category',
                           choices=['Aventuras', 'Ciencia ficción', 'Policíaca', 'Terror', 'Romántica', 'Humor'])
    image = FileField('Image')
    author = StringField('Author', validators=[DataRequired(), Length(min=5)])
    num_of_pages = IntegerField('Num of pages', validators=[DataRequired()])
    submit = SubmitField('Update')
