import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from Bl.User import User
from Bl.UserManager import UserManager
from Bl.CinemaBl import CinemaBl
from Bl.Theater import Theater
from Bl.Seat import Seat
from Bl.Movie import Movie
from Bl.MockData import MockData

class TestUser(unittest.TestCase):
    def setUp(self) -> None:
        self.user = User("testuser", "password")

    def test_add_ticket(self) -> None:
        self.user.add_ticket("Test Ticket")
        self.assertIn("Test Ticket", self.user.tickets)

    def test_add_ticket_empty(self) -> None:
        with self.assertRaises(ValueError):
            self.user.add_ticket("")

    def test_view_tickets(self) -> None:
        self.user.add_ticket({'movie': 'Avatar', 'theater': 'Theater 1', 'showtime': '10:00', 'row': 0, 'col': 0})
        self.user.add_ticket({'movie': 'Avatar', 'theater': 'Theater 1', 'showtime': '10:00', 'row': 1, 'col': 0})
        tickets = self.user.view_tickets()
        self.assertEqual(tickets, [
            "Movie: Avatar, Theater: Theater 1, Showtime: 10:00, Seat: 1:A",
            "Movie: Avatar, Theater: Theater 1, Showtime: 10:00, Seat: 2:A"
        ])

class TestUserManager(unittest.TestCase):
    def setUp(self) -> None:
        self.user_manager = UserManager()
        self.cinema_bl = CinemaBl()

    def test_register_user(self) -> None:
        self.user_manager.register("test_user", "password")
        self.assertIn("test_user", self.user_manager.users)

    def test_register_existing_user(self) -> None:
        self.user_manager.register("test_user", "password")
        with self.assertRaises(ValueError):
            self.user_manager.register("test_user", "password")

    def test_login_user(self) -> None:
        self.user_manager.register("test_user", "password")
        self.user_manager.login("test_user", "password")
        self.assertEqual(self.user_manager.current_user.username, "test_user")

    def test_login_invalid_user(self) -> None:
        with self.assertRaises(ValueError):
            self.user_manager.login("invalid_user", "password")

    def test_login_incorrect_password(self) -> None:
        self.user_manager.register("test_user", "password")
        with self.assertRaises(ValueError):
            self.user_manager.login("test_user", "wrong_password")

    def test_book_ticket(self) -> None:
        self.user_manager.register("test_user", "password")
        self.user_manager.login("test_user", "password")
        self.user_manager.book_ticket("Avatar", "Theater 1", "10:00", 1, 1, self.cinema_bl)
        self.assertEqual(len(self.user_manager.current_user.tickets), 1)

    def test_book_ticket_invalid_movie(self) -> None:
        self.user_manager.register("test_user", "password")
        self.user_manager.login("test_user", "password")
        with self.assertRaises(Exception):
            self.user_manager.book_ticket("Invalid Movie", "Theater 1", "10:00", 1, 1, self.cinema_bl)

    def test_book_ticket_invalid_theater(self) -> None:
        self.user_manager.register("test_user", "password")
        self.user_manager.login("test_user", "password")
        with self.assertRaises(Exception):
            self.user_manager.book_ticket("Avatar", "Invalid Theater", "10:00", 1, 1, self.cinema_bl)

    def test_book_ticket_invalid_seat(self) -> None:
        self.user_manager.register("test_user", "password")
        self.user_manager.login("test_user", "password")
        with self.assertRaises(ValueError):
            self.user_manager.book_ticket("Avatar", "Theater 1", "10:00", -1, 1, self.cinema_bl)

    def test_register_user_empty_username(self) -> None:
        with self.assertRaises(ValueError):
            self.user_manager.register("", "password")

    def test_register_user_empty_password(self) -> None:
        with self.assertRaises(ValueError):
            self.user_manager.register("test_user", "")

    def test_login_user_empty_username(self) -> None:
        with self.assertRaises(ValueError):
            self.user_manager.login("", "password")

    def test_login_user_empty_password(self) -> None:
        with self.assertRaises(ValueError):
            self.user_manager.login("test_user", "")

    def test_book_ticket_empty_movie(self) -> None:
        self.user_manager.register("test_user", "password")
        self.user_manager.login("test_user", "password")
        with self.assertRaises(ValueError):
            self.user_manager.book_ticket("", "Theater 1", "10:00", 1, 1, self.cinema_bl)

    def test_book_ticket_empty_theater(self) -> None:
        self.user_manager.register("test_user", "password")
        self.user_manager.login("test_user", "password")
        with self.assertRaises(ValueError):
            self.user_manager.book_ticket("Avatar", "", "10:00", 1, 1, self.cinema_bl)

    def test_book_ticket_empty_showtime(self) -> None:
        self.user_manager.register("test_user", "password")
        self.user_manager.login("test_user", "password")
        with self.assertRaises(ValueError):
            self.user_manager.book_ticket("Avatar", "Theater 1", "", 1, 1, self.cinema_bl)

class TestTheater(unittest.TestCase):
    def setUp(self) -> None:
        self.theater = Theater(5, 5)
        self.theater.setup_showtimes(["10:00", "14:00"])

    def test_setup_showtimes(self) -> None:
        self.assertIn("10:00", self.theater.showtime_seating)
        self.assertIn("14:00", self.theater.showtime_seating)

    def test_display_seats(self) -> None:
        seat_display = self.theater.display_seats("10:00")
        self.assertEqual(len(seat_display), 8)

    def test_book_seat(self) -> None:
        self.theater.book_seat(1, 1, "10:00")
        self.assertTrue(self.theater.showtime_seating["10:00"][1][1].is_booked)

    def test_book_seat_invalid_showtime(self) -> None:
        with self.assertRaises(Exception):
            self.theater.book_seat(1, 1, "Invalid Showtime")

    def test_book_seat_invalid_position(self) -> None:
        with self.assertRaises(ValueError):
            self.theater.book_seat(-1, 1, "10:00")

    def test_book_seat_already_booked(self) -> None:
        self.theater.book_seat(1, 1, "10:00")
        with self.assertRaises(Exception):
            self.theater.book_seat(1, 1, "10:00")

class TestSeat(unittest.TestCase):
    def setUp(self) -> None:
        self.seat = Seat(1, 1)

    def test_initial_state(self) -> None:
        self.assertFalse(self.seat.is_booked)

    def test_display_unbooked(self) -> None:
        self.assertEqual(self.seat.display(), "\U0001FA91")

    def test_display_booked(self) -> None:
        self.seat.book()
        self.assertEqual(self.seat.display(), "❌")

    def test_book_seat(self) -> None:
        self.seat.book()
        self.assertTrue(self.seat.is_booked)

    def test_book_already_booked_seat(self) -> None:
        self.seat.book()
        with self.assertRaises(Exception):
            self.seat.book()

class TestMovie(unittest.TestCase):
    def setUp(self) -> None:
        self.movie = Movie("Avatar")

    def test_initial_state(self) -> None:
        self.assertEqual(self.movie.title, "Avatar")
        self.assertEqual(self.movie.theaters, {})

    def test_add_showtime(self) -> None:
        self.movie.add_showtime("Theater 1", ["10:00", "14:00"])
        self.assertIn("Theater 1", self.movie.theaters)
        self.assertEqual(self.movie.theaters["Theater 1"], ["10:00", "14:00"])

    def test_add_showtime_empty_theater(self) -> None:
        with self.assertRaises(ValueError):
            self.movie.add_showtime("", ["10:00", "14:00"])

    def test_add_showtime_empty_showtimes(self) -> None:
        with self.assertRaises(ValueError):
            self.movie.add_showtime("Theater 1", [])

    def test_get_theaters(self) -> None:
        self.movie.add_showtime("Theater 1", ["10:00", "14:00"])
        self.assertEqual(self.movie.get_theaters(), ["Theater 1"])

    def test_get_showtimes(self) -> None:
        self.movie.add_showtime("Theater 1", ["10:00", "14:00"])
        self.assertEqual(self.movie.get_showtimes("Theater 1"), ["10:00", "14:00"])

    def test_add_showtime_invalid_showtime(self) -> None:
        with self.assertRaises(ValueError):
            self.movie.add_showtime("Theater 1", [" "])

class TestCinemaBl(unittest.TestCase):
    def setUp(self) -> None:
        self.cinema_bl = CinemaBl()
        self.user = User("testuser", "password")

    def test_load_theaters(self) -> None:
        self.assertIn("Theater 1", self.cinema_bl.get_theaters())
        self.assertIn("Theater 2", self.cinema_bl.get_theaters())

    def test_load_movies(self) -> None:
        self.assertIn("Avatar", self.cinema_bl.get_movies())
        self.assertIn("Titanic", self.cinema_bl.get_movies())

    def test_get_movies(self) -> None:
        movies = self.cinema_bl.get_movies()
        self.assertEqual(len(movies), 2)

    def test_get_theaters(self) -> None:
        theaters = self.cinema_bl.get_theaters()
        self.assertEqual(len(theaters), 2)


if __name__ == "__main__":
    unittest.main()
