import os
import uuid
from pathlib import Path


def upload_file(file, filename):
    path = Path.joinpath(Path(__file__).parent.parent, 'static/images')
    file.save(Path.joinpath(path, filename))


def delete_file(filename):
    path = Path.joinpath(Path(__file__).parent.parent, 'static/images')
    os.remove(Path.joinpath(path, filename))


class Book:
    id = str(uuid.uuid4())

    def __init__(self, title, isbn, category, filename, author, num_of_pages, user_id):
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
