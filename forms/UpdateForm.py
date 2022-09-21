from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import Length, DataRequired, ValidationError

from models.book import book_list


def unique_title(form, field):
    for book in book_list:
        if book.field == field.data:
            raise ValidationError('This title already exist', 422)

    return True


def unique_isbn(form, field) -> bool:
    for book in book_list:
        if book.field == field.data:
            raise ValidationError('This ISBN already exist', 422)

    return True


class UpdateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3)])
    isbn = StringField('ISBN', validators=[DataRequired()])
    category = SelectField('Category',
                           choices=['Aventuras', 'Ciencia ficción', 'Policíaca', 'Terror', 'Romántica', 'Humor'])
    image = FileField('Image')
    author = StringField('Author', validators=[DataRequired(), Length(min=5)])
    num_of_pages = IntegerField('Num of pages', validators=[DataRequired()])
    submit = SubmitField('Update')
