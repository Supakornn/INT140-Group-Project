import curses
from library import Library
from book import Book
from user import User
from library_ui import LibraryUI

def main(stdscr):
    library = Library()
    book1 = Book(book_id=1, title="Introduction to Python", author="John Doe")
    book2 = Book(book_id=2, title="Advanced Python Programming", author="Jane Smith")
    user1 = User(user_id=1, name="Alice")
    user2 = User(user_id=2, name="Bob")

    library.add_book(book1)
    library.add_book(book2)
    library.add_user(user1)
    library.add_user(user2)

    ui = LibraryUI(stdscr, library)

    ui.handle_login()
    ui.handle_user_actions()  

curses.wrapper(main)
