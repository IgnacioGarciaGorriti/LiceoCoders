from pathlib import Path

from flask import make_response

book_list: list = []


def get(book_id: int):
    for book in book_list:
        if book.id == book_id:
            return book

    return None


def delete(book_id: int):
    for [index, book] in enumerate(book_list):
        if book.id == book_id:
            del book_list[index]
            return

    raise ValueError(f"Book with id: {book_id} doesn't exist", 404)


def upload_file(file, filename):
    path = Path.joinpath(Path(__file__).parent.parent, 'static/images')
    file.save(Path.joinpath(path, filename))


def update(book_id: int, params: dict):
    for book in book_list:
        if book.id == book_id:
            book.isbn = params['isbn']
            book.title = params['title']
            book.category = params['category']
            book.author = params['author']
            book.num_of_pages = params['num_of_pages']
            if 'filename' in params.keys():
                book.filename = params['filename']

        return book.to_json('show')

    raise ValueError(f"Book with id: {book_id} doesn't exist", 404)


class Book:

    def __init__(self, title, isbn, category, filename, author, num_of_pages, user_id):
        latest_id = max(book_list, key=lambda x: x.id, default=0)
        if latest_id == 0:
            self.id = 1
        else:
            self.id = latest_id.id + 1
        self.title: str = title
        self.isbn: str = isbn
        self.category: str = category
        self.filename: str = filename
        self.author: str = author
        self.num_of_pages: int = num_of_pages
        self.user_id: str = user_id

    def to_json(self, type: str):
        if type == 'list':
            return {
                'id': self.id,
                'title': self.title,
                'author': self.author,
                'user_id': self.user_id
            }
        elif type == 'show':
            return {
                'id': self.id,
                'title': self.title,
                'author': self.author,
                'isbn': self.isbn,
                'category': self.category,
                'num_of_pages': self.num_of_pages
            }
