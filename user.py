class User:
    def __init__(self, user_id: int, name: str):
        self.user_id = user_id
        self.name = name
        self.borrowed_books = []

    def show_info(self):
        print(f"User: {self.name}")
        print("Borrowed Books:")
        if not self.borrowed_books:
            print("No books borrowed.")
        else:
            for book in self.borrowed_books:
                print(f"- {book.title} (Returned: {book.is_borrowed})")
