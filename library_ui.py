import curses
from user import User
from book import Book
from library import Library

class LibraryUI:
    def __init__(self, stdscr, library: Library):
        self.stdscr = stdscr
        self.library = library
        self.current_user = None

    def display_main_menu(self):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "Library System", curses.A_BOLD)
        self.stdscr.addstr(2, 0, "1. Login as Alice")
        self.stdscr.addstr(3, 0, "2. Login as Bob")
        self.stdscr.addstr(4, 0, "3. Exit")
        self.stdscr.addstr(6, 0, "Choose an option:")
        self.stdscr.refresh()

    def handle_login(self):
        self.stdscr.clear()
        self.display_main_menu()

        while True:
            key = self.stdscr.getkey()
            if key == '1':
                self.current_user = self.library.users[0]  # Alice
                break
            elif key == '2':
                self.current_user = self.library.users[1]  # Bob
                break
            elif key == '3':
                exit()

    def display_user_menu(self):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, f"Welcome {self.current_user.name}!")
        self.stdscr.addstr(2, 0, "1. Borrow Book")
        self.stdscr.addstr(3, 0, "2. Return Book")
        self.stdscr.addstr(4, 0, "3. Show Info")
        self.stdscr.addstr(5, 0, "4. Logout")
        self.stdscr.addstr(7, 0, "Choose an option:")
        self.stdscr.refresh()

    def handle_user_actions(self):
        while True:
            self.stdscr.clear()
            self.display_user_menu()

            key = self.stdscr.getkey()
            if key == '1':
                self.borrow_book()
            elif key == '2':
                self.return_book()
            elif key == '3':
                self.show_user_info()
            elif key == '4':
                break  # Logout

    def borrow_book(self):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "Select a book to borrow:")
        self.stdscr.addstr(1, 0, f"1. {self.library.books[0].title} by {self.library.books[0].author}")
        self.stdscr.addstr(2, 0, f"2. {self.library.books[1].title} by {self.library.books[1].author}")
        self.stdscr.addstr(3, 0, "Choose an option:")
        self.stdscr.refresh()

        book_choice = self.stdscr.getkey()
        if book_choice == '1':
            self.library.borrow_book(book_id=1, user_id=self.current_user.user_id)
        elif book_choice == '2':
            self.library.borrow_book(book_id=2, user_id=self.current_user.user_id)

        self.stdscr.addstr(5, 0, "Press any key to continue...")
        self.stdscr.refresh()
        self.stdscr.getkey()

    def return_book(self):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "Select a book to return:")
        self.stdscr.addstr(1, 0, f"1. {self.library.books[0].title} by {self.library.books[0].author}")
        self.stdscr.addstr(2, 0, f"2. {self.library.books[1].title} by {self.library.books[1].author}")
        self.stdscr.addstr(3, 0, "Choose an option:")
        self.stdscr.refresh()

        book_choice = self.stdscr.getkey()
        if book_choice == '1':
            self.library.return_book(book_id=1, user_id=self.current_user.user_id)
        elif book_choice == '2':
            self.library.return_book(book_id=2, user_id=self.current_user.user_id)

        self.stdscr.addstr(5, 0, "Press any key to continue...")
        self.stdscr.refresh()
        self.stdscr.getkey()

    def show_user_info(self):
        self.stdscr.clear()
        self.current_user.show_info()
        self.stdscr.addstr(7, 0, "Press any key to continue...")
        self.stdscr.refresh()
        self.stdscr.getkey()
