from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import Length, DataRequired, ValidationError

from models.book import book_list


def unique_title(form, field):
    for book in book_list:
        if book.title == field.data:
            raise ValidationError('This title already exist', 422)

    return True


def unique_isbn(form, field) -> bool:
    for book in book_list:
        if book.isbn == field.data:
            raise ValidationError('This ISBN already exist', 422)

    return True


class CreateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3), unique_title])
    isbn = StringField('ISBN', validators=[DataRequired(), unique_isbn])
    category = SelectField('Category',
                           choices=['Aventuras', 'Ciencia ficción', 'Policíaca', 'Terror', 'Romántica', 'Humor'])
    image = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg', 'png'])])
    author = StringField('Author', validators=[DataRequired(), Length(min=5)])
    num_of_pages = IntegerField('Num of pages', validators=[DataRequired()])
    submit = SubmitField('Add')
