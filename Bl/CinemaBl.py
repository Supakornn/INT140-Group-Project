from typing import Dict
from Bl.MockData import MockData
from Bl.Movie import Movie
from Bl.Theater import Theater
from Bl.User import User

class CinemaBl:
    def __init__(self):
        self.theaters: Dict[str, Theater] = {}  # Theater -> Theater
        self.movies: Dict[str, Movie] = {}  # Movie_title -> Movie
        self.load_theaters()
        self.load_movies()

    def load_theaters(self) -> None:
        for theater_name, config in MockData.THEATERS.items():
            if not theater_name or not config:
                raise ValueError("Theater name and config cannot be empty.")
            self.theaters[theater_name] = Theater(config["rows"], config["cols"])

    def load_movies(self) -> None:
        for movie_title, theaters in MockData.MOVIES.items():
            if not movie_title or not theaters:
                raise ValueError("Movie title and theaters cannot be empty.")
            movie = Movie(movie_title)
            for theater_name, showtimes in theaters.items():
                movie.add_showtime(theater_name, showtimes)
                if theater_name in self.theaters:
                    self.theaters[theater_name].setup_showtimes(showtimes)
            self.movies[movie_title] = movie

    def get_movies(self) -> Dict[str, Movie]:
        return self.movies

    def get_theaters(self) -> Dict[str, Theater]:
        return self.theaters

    def display_user_tickets(self, user: User) -> None:
        tickets = user.view_tickets()
        print(f"--- Tickets for {user.username} ---")
        for ticket in tickets:
            print(ticket)
