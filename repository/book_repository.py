from models.book import Book
from repository.abstract_repository import AbstractRepository
import models.book


class BookRepository(AbstractRepository):
    models.book.Base.metadata.create_all(super().engine, checkfirst=True)

    def get(self, book_id):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute('select * from book where id = %s', (book_id,))
        book = self.__compound_book(cursor.fetchone())
        cursor.close()
        return book

    def get_by_title_and_user_id(self, title, user_id):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute('select * from book where title = %s and user_id = %s limit 1', (title, user_id))
        book = self.__compound_book(cursor.fetchone())
        cursor.close()
        return book

    def get_by_isbn_and_user_id(self, isbn, user_id):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute('select * from book where isbn = %s and user_id = %s limit 1', (isbn, user_id))
        book = self.__compound_book(cursor.fetchone())
        cursor.close()
        return book

    def list(self):
        book_list = []
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute('select * from book')
        rows = cursor.fetchall()
        for row in rows:
            book_list.append(self.__compound_book(row))
        cursor.close()
        return book_list

    def add(self, book: Book):
        cursor = self.connection.cursor()
        cursor.execute('insert into book values (%s, %s, %s, %s, %s, %s, %s, %s)',
                       (
                           book.id,
                           book.title,
                           book.isbn,
                           book.category,
                           book.filename,
                           book.author,
                           book.num_of_pages,
                           book.user_id
                       ))
        self.connection.commit()
        cursor.close()

    def update(self, book_id, params):
        cursor = self.connection.cursor()
        if 'filename' in params.keys():
            cursor.execute(
                'update book set title = %s, isbn = %s, category = %s, author = %s, num_of_pages = %s, filename = %s where id = %s',
                (
                    params["title"],
                    params["isbn"],
                    params["category"],
                    params["author"],
                    params["num_of_pages"],
                    params["filename"],
                    book_id
                ))
        else:
            cursor.execute('update book set title = %s, isbn = %s, category = %s, author = %s, num_of_pages = %s where id = %s',
                           (
                                params["title"],
                                params["isbn"],
                                params["category"],
                                params["author"],
                                params["num_of_pages"],
                                book_id
                           ))
        self.connection.commit()
        cursor.close()

    def delete(self, book_id):
        cursor = self.connection.cursor()
        cursor.execute('delete from book where id = %s', (book_id,))
        self.connection.commit()
        cursor.close()

    def __compound_book(self, row):
        if row is None:
            return None

        book = Book(
            row['title'],
            row['isbn'],
            row['category'],
            row['filename'],
            row['author'],
            row['num_of_pages'],
            row['user_id']
        )
        book.id = row['id']

        return book
