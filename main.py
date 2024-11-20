

from library import Library
from book import Book
from user import User

library = Library()
book1 = Book(1, "The Great Gatsby", "F. Scott Fitzgerald")
book2 = Book(2, "The Catcher in the Rye", "J.D. Salinger")
book3 = Book(3, "To Kill a Mockingbird", "Harper Lee")
library.add_book(book1)
library.add_book(book2)
library.add_book(book3)
user1 = User(1, "Alice")
user2 = User(2, "Bob")
library.add_user(user1)
library.add_user(user2)
library.borrow_book(1, 1)
library.borrow_book(2, 2)

print(user1)
library.return_book(1, 1)
print(user1)