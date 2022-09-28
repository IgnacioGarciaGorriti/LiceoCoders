import os
import uuid
from pathlib import Path
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base
import models.user

def upload_file(file, filename):
    path = Path.joinpath(Path(__file__).parent.parent, 'static/images')
    file.save(Path.joinpath(path, filename))


def delete_file(filename):
    path = Path.joinpath(Path(__file__).parent.parent, 'static/images')
    os.remove(Path.joinpath(path, filename))


class Book(Base):
    __tablename__ = 'book'
    id = Column(String(255), primary_key=True)
    title = Column(String(255))
    isbn = Column(String(255))
    category = Column(String(255))
    filename = Column(String(255))
    author = Column(String(255))
    num_of_pages = Column(Integer)
    user_id = Column(String(255), ForeignKey("users.id"))
    user = relationship("User", back_populates="books")

    def __init__(self, title, isbn, category, filename, author, num_of_pages, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id = str(uuid.uuid4())
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
