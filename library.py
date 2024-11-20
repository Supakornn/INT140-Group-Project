from user import User
from book import Book

class Library:
    def __init__(self):
        self.books = []
        self.users = []

    def add_book(self, book: Book):
        self.books.append(book)

    def add_user(self, user: User):
        self.users.append(user)

    def borrow_book(self, book_id: int, user_id: int):
        book = next((b for b in self.books if b.book_id == book_id), None)
        user = next((u for u in self.users if u.user_id == user_id), None)
        
        if book and user:
            book.is_borrowed = True
            user.borrowed_books.append(book)

    def return_book(self, book_id: int, user_id: int):
        book = next((b for b in self.books if b.book_id == book_id), None)
        user = next((u for u in self.users if u.user_id == user_id), None)
        if book and user and book in user.borrowed_books:
            book.is_borrowed = False
            user.borrowed_books.remove(book)
