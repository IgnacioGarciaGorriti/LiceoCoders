from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, IntegerField, SelectField, SubmitField, HiddenField
from wtforms.validators import Length, DataRequired, ValidationError
from repository.book_repository import BookRepository


def unique_title(form, field):
    book_repository = BookRepository()
    book = book_repository.get_by_title_and_user_id(field.data, current_user.id)
    if book is None or book.id == form.id.data:
        return True
    raise ValidationError('This title already exist', 422)


def unique_isbn(form, field) -> bool:
    book_repository = BookRepository()
    book = book_repository.get_by_isbn_and_user_id(field.data, current_user.id)
    if book is None or book.id == form.id.data:
        return True
    raise ValidationError('This ISBN already exist', 422)


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
