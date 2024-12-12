from typing import Dict, Optional
from Bl.User import User
from Bl.CinemaBl import CinemaBl

class UserManager:
    def __init__(self):
        self.users: Dict[str, User] = {} 
        self.current_user: Optional[User] = None

    def register(self, username: str, password: str) -> None:
        self._validate_credentials(username, password)
        if username in self.users:
            raise ValueError("Username already exists!")
        self.users[username] = User(username, password)

    def login(self, username: str, password: str) -> None:
        self._validate_credentials(username, password)
        if username not in self.users:
            raise ValueError("Username not found.")
        if self.users[username].password != password:
            raise ValueError("Incorrect password.")
        self.current_user = self.users[username]

    def logout(self) -> None:
        self.current_user = None

    def book_ticket(self, movie_title: str, theater_name: str, showtime: str, row: int, col: int, cinema_bl: CinemaBl) -> None:
        self._validate_booking(movie_title, theater_name, showtime, row, col, cinema_bl)
        theater = cinema_bl.get_theaters()[theater_name]
        theater.book_seat(row, col, showtime)
        ticket = {
            "movie": movie_title,
            "theater": theater_name,
            "showtime": showtime,
            "row": row,
            "col": col
        }
        self.current_user.add_ticket(ticket)

    def _validate_credentials(self, username: str, password: str) -> None:
        if not username or not password:
            raise ValueError("Username and password cannot be empty.")

    def _validate_booking(self, movie_title: str, theater_name: str, showtime: str, row: int, col: int, cinema_bl: CinemaBl) -> None:
        if self.current_user is None:
            raise Exception("No user is currently logged in.")
        if not movie_title or not theater_name or not showtime:
            raise ValueError("Movie title, theater name, and showtime cannot be empty.")
        if movie_title not in cinema_bl.get_movies():
            raise Exception("Movie not found.")
        if theater_name not in cinema_bl.get_theaters():
            raise Exception("Theater not found.")
        theater = cinema_bl.get_theaters()[theater_name]
        if row < 0 or row >= theater.rows or col < 0 or col >= theater.cols:
            raise ValueError("Invalid seat position.")
