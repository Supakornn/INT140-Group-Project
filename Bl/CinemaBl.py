from Bl.MockData import MockData
from Bl.Movie import Movie
from Bl.Theater import Theater
from Bl.User import User
import string

class CinemaBl:
    def __init__(self):
        self.users = {}  # username -> User
        self.current_user = None
        self.theaters = {}  # Theater -> Theater
        self.movies = {}  # Movie_title -> Movie
        self.load_theaters()
        self.load_movies()
        
    #load theaters and movies data
    def load_theaters(self):
        for theater_name, config in MockData.THEATERS.items():
            self.theaters[theater_name] = Theater(config["rows"], config["cols"])

    def load_movies(self):
        for movie_title, theaters in MockData.MOVIES.items():
            movie = Movie(movie_title)
            for theater_name, showtimes in theaters.items():
                movie.add_showtime(theater_name, showtimes)
                if theater_name in self.theaters:
                    self.theaters[theater_name].setup_showtimes(showtimes)
            self.movies[movie_title] = movie
    
    def register(self, username, password):
        if username in self.users:
            raise ValueError("Username already exists! Please try again.")
        self.users[username] = User(username, password)
        
    def login(self, username, password):
        if username not in self.users:
            raise ValueError("Username not found. Please try again.")
        if self.users[username].password != password:
            raise ValueError("Incorrect password. Please try again.")
        self.current_user = self.users[username]
        return self.current_user
    
    def get_current_user(self):
        return self.current_user
    
    def logout(self):
        self.current_user = None

    def get_all_movie(self):
        return self.movies.keys()
    
    
    def validate_movie_idx(self, movie_idx):
        movie_titles = list(self.movies.keys())
        if movie_idx is None:
            raise ValueError("Movie not found. Please try again.")
        movie_idx = int(movie_idx)-1
        if movie_idx < 0 or movie_idx >= len(self.movies):
            raise ValueError("Movie not found. Please try again.")
        if movie_titles[movie_idx] not in self.movies:
            raise ValueError("Movie not found. Please try again.")
        return movie_idx
    
    def get_movie(self, movie_idx):
        movie_titles = list(self.movies.keys())
        try:
            movie_idx = self.validate_movie_idx(movie_idx)
            movie_title = movie_titles[movie_idx]
            return self.movies[movie_title]
        except Exception as e:
            raise e
    
    def get_theaters_for_movie(self,movie):
        return movie.get_theaters()
    
    def validate_theater_idx(self,movie, theater_idx):
        theaters = self.get_theaters_for_movie(movie)
        theater_names = list(theaters.keys())
        if theater_idx is None:
            raise ValueError("Theater not found. Please try again.")
        theater_idx = int(theater_idx)-1
        if theater_idx < 0 or theater_idx >= len(theater_names):
            raise ValueError("Theater not found. Please try again.")
        if theater_names[theater_idx] not in theaters:
            raise ValueError("Theater not found. Please try again.")
        return theater_idx
    
    def get_theater(self,movie, theater_idx):
        theater_names = list(self.get_theaters_for_movie(movie).keys())
        try:
            theater_idx = self.validate_theater_idx(movie, theater_idx)
            theater_name = theater_names[theater_idx]
            return self.theaters[theater_name]
        except Exception as e:
            raise e
        
    def get_showtimes_for_theater(self,movie,theater):
        return movie.get_showtimes(theater)
        
    def validate_showtime_idx(self,movie,theater, showtime_idx):
        showtimes = self.get_showtimes_for_theater(movie,theater)
        if showtime_idx is None:
            raise ValueError("Showtime not found. Please try again.")
        showtime_idx = int(showtime_idx)-1
        if showtime_idx < 0 or showtime_idx >= len(showtimes):
            raise ValueError("Showtime not found. Please try again.")
        return showtime_idx
    
    def get_showtime(self,movie,theater, showtime_idx):
        showtimes = self.get_showtimes_for_theater(movie,theater)
        try:
            showtime_idx = self.validate_showtime_idx(movie,theater, showtime_idx)
            return showtimes[showtime_idx]
        except Exception as e:
            raise e
        
    def display_seats(self,theater,showtime):
        return theater.display_seats(showtime)
    
    def book_ticket(self,theater,showtime,row,col):
        return theater.book_seat(row, col, showtime)
