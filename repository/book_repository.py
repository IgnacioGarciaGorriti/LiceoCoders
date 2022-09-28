from models.book import Book
from repository.abstract_repository import AbstractRepository
import models.book


class BookRepository(AbstractRepository):
    def get(self, book_id):
        return self.session.query(Book).filter_by(id=book_id).one_or_none()

    def get_by_title_and_user_id(self, title, user_id):
        return self.session.query(Book).filter_by(title=title, user_id=user_id).one_or_none()

    def get_by_isbn_and_user_id(self, isbn, user_id):
        return self.session.query(Book).filter_by(isbn=isbn, user_id=user_id).one_or_none()

    def list(self):
        return self.session.query(Book).all()

    def add(self, book: Book):
        self.session.add(book)
        self.session.commit()

    def update(self, book, params):
        book.title = params["title"]
        book.isbn = params["isbn"]
        book.category = params["category"]
        book.author = params["author"]
        book.num_of_pages = params["num_of_pages"]
        if 'filename' in params.keys():
            book.filename = params["filename"]
        self.session.commit()

    def delete(self, book):
        self.session.delete(book)
        self.session.commit()
