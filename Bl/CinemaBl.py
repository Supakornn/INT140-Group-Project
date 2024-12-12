from typing import Dict
from Bl.MockData import MockData
from Bl.Movie import Movie
from Bl.Theater import Theater
from Bl.User import User

class CinemaBl:
    def __init__(self):
        self.theaters: Dict[str, Theater] = {} 
        self.movies: Dict[str, Movie] = {} 
        self.load_theaters()
        self.load_movies()

    def load_theaters(self) -> None:
        for theater_name, config in MockData.THEATERS.items():
            self._validate_theater_data(theater_name, config)
            self.theaters[theater_name] = Theater(config["rows"], config["cols"])

    def load_movies(self) -> None:
        for movie_title, theaters in MockData.MOVIES.items():
            self._validate_movie_data(movie_title, theaters)
            movie = Movie(movie_title)
            self._setup_movie_showtimes(movie, theaters)
            self.movies[movie_title] = movie

    def _validate_theater_data(self, theater_name: str, config: dict) -> None:
        if not theater_name or not config:
            raise ValueError("Theater name and config cannot be empty.")

    def _validate_movie_data(self, movie_title: str, theaters: dict) -> None:
        if not movie_title or not theaters:
            raise ValueError("Movie title and theaters cannot be empty.")

    def _setup_movie_showtimes(self, movie: Movie, theaters: dict) -> None:
        for theater_name, showtimes in theaters.items():
            movie.add_showtime(theater_name, showtimes)
            if theater_name in self.theaters:
                self.theaters[theater_name].setup_showtimes(showtimes)

    def get_movies(self) -> Dict[str, Movie]:
        return self.movies

    def get_theaters(self) -> Dict[str, Theater]:
        return self.theaters

    def display_user_tickets(self, user: User) -> None:
        tickets = user.view_tickets()
        print(f"--- Tickets for {user.username} ---")
        for ticket in tickets:
            print(ticket)
