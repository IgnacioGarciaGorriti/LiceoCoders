import os
import uuid

from flask import Blueprint, render_template, make_response, redirect, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from forms.CreateForm import CreateForm
from forms.UpdateForm import UpdateForm
from models.book import Book, upload_file, delete_file
from repository.book_repository import BookRepository

books = Blueprint('books', __name__, url_prefix='/books')


@books.get('/<book_id>')
@login_required
def show(book_id):
    try:
        book_repository = BookRepository()
        book = book_repository.get(book_id)

        if book is None:
            raise ValueError(f"Book with id {book_id} doesn't exist")

        return render_template('books/show.html', book=book)
    except Exception as e:
        return make_response(e.__str__(), 400)


@books.get('/')
@login_required
def display_list():
    try:
        user = current_user
        book_repository = BookRepository()
        book_list = book_repository.list()
        list_books = [book.to_json('list') for book in book_list]

        return render_template('books/list.html', list_books=list_books, user=user)
    except Exception as e:
        return make_response(e.__str__(), 400)


@books.get('/update/<book_id>')
@login_required
def update_template(book_id):
    try:
        book_repository = BookRepository()
        book = book_repository.get(book_id)
        form = UpdateForm(obj=book)

        return render_template('books/edit.html', form=form)
    except Exception as e:
        return make_response(e.__str__(), 400)


@books.post('/update/<book_id>')
@login_required
def update_book(book_id):
    try:
        form = UpdateForm()
        if form.validate_on_submit():
            params = {
                'title': form.title.data,
                'isbn': form.isbn.data,
                'category': form.category.data,
                'author': form.author.data,
                'num_of_pages': form.num_of_pages.data,
            }

            if form.image.data is not None:
                filename = str(uuid.uuid4()) + '_' + secure_filename(form.image.data.filename)
                params['filename'] = filename
                upload_file(form.image.data, filename)

            book_repository = BookRepository()
            book = book_repository.get(book_id)

            if book is None:
                raise ValueError(f"Book with id: {book_id} doesn't exist", 404)

            if book.user_id != current_user.id:
                raise ValueError("Unauthorized", 401)

            book_repository.update(book_id, params)

            return redirect(url_for('books.show', book_id=book_id))

        return render_template('books/edit.html', form=form)
    except Exception as e:
        return make_response(e.__str__(), 400)


@books.get('/add')
@login_required
def add_template():
    form = CreateForm()
    return render_template('books/add.html', form=form)


@books.post('/add')
@login_required
def add_book():
    try:
        form = CreateForm()

        if form.validate_on_submit():
            title = form.title.data
            isbn = form.isbn.data
            category = form.category.data
            author = form.author.data
            filename = str(uuid.uuid4()) + '_' + secure_filename(form.image.data.filename)
            upload_file(form.image.data, filename)
            num_of_pages = form.num_of_pages.data
            user_id = current_user.id

            book = Book(title, isbn, category, filename, author, num_of_pages, user_id)
            book_repository = BookRepository()
            book_repository.add(book)

            return redirect(url_for('books.show', book_id=book.id))

        return render_template('books/add.html', form=form)
    except Exception as e:
        return make_response(e.__str__(), 400)


@books.delete('/delete/<book_id>')
@login_required
def remove_book(book_id):
    try:
        book_repository = BookRepository()
        book = book_repository.get(book_id)
        if book is None:
            raise ValueError(f"Book with id: {book_id} doesn't exist", 404)
        if book.user_id != current_user.id:
            raise ValueError("Unauthorized", 401)

        delete_file(book.filename)
        book_repository.delete(book_id)

        return make_response('book deleted', 200)

    except Exception as e:
        return make_response(e.__str__(), 400)
