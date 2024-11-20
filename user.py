class User:
    def __init__(self, user_id: int, name: str):
        self.user_id = user_id
        self.name = name
        self.borrowed_books = []

    def __str__(self):
        return f"User ID: {self.user_id}, Name: {self.name}, Borrowed Books: {[book.title for book in self.borrowed_books]}"
