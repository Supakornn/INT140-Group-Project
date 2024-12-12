from Bl.MockData import MockData
from Bl.Movie import Movie
from Bl.Theater import Theater
from Bl.User import User
import string

class CinemaApp:
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

    def register(self):
        while True:
            username = input("Enter username (or type 'exit' to cancel): ")
            if username.lower() == 'exit':
                print("Exiting registration!")
                return
            if username in self.users:
                print("Username already exists! Please try again.")
                continue
            password = input("Enter password: (or type 'exit' to cancel): ")
            if password.lower() == 'exit':
                print("Exiting registration!")
                return
            self.users[username] = User(username, password)
            print("User registered successfully!")
            return

    def login(self):
        while True:
            username = input("Enter username (or type 'exit' to cancel): ")
            if username.lower() == 'exit':
                print("Exiting login!")
                return
            if username not in self.users:
                print("Username not found. Please try again.")
                continue
            password = input("Enter password: (or type 'exit' to cancel): ")
            if password.lower() == 'exit':
                print("Exiting login!")
                return
            if self.users[username].password != password:
                print("Incorrect password. Please try again.")
                continue
            self.current_user = self.users[username]
            print(f"Welcome, {username}!")
            break

    def logout(self):
        self.current_user = None
        print("Logout success!")

    def view_movies(self):
        print("\n--- Movies in Cinema ---")
        for idx, (movie_title, movie) in enumerate(self.movies.items(), start=1):
            print(f"{idx}. {movie_title}:")
            for theater_name, showtimes in movie.theaters.items():
                print(f"  {theater_name}: {', '.join(showtimes)}")

    def book_ticket(self):
        if not self.current_user:
            print("Please log in to book a ticket!")
            return

        # Select Movie
        print("\n--- Select a Movie ---")
        movie_titles = list(self.movies.keys())
        for idx, movie_title in enumerate(movie_titles, start=1):
            print(f"{idx}. {movie_title}")

        try:
            movie_idx = input("Enter movie index: (or type 'exit' to cancel): ")
            if movie_idx.lower() == 'exit':
                print("Exiting ticket booking!")
            movie_idx = int(movie_idx) - 1
            if movie_idx < 0:
                raise ValueError
            if movie_idx >= len(movie_titles):
                raise IndexError
            movie_title = movie_titles[movie_idx]
        except (ValueError, IndexError):
            print("Invalid input!")
            return

        movie = self.movies[movie_title]

        # Select theater
        print("\n--- Select a Theater ---")
        theaters = list(movie.get_theaters())
        for idx, theater_name in enumerate(theaters, start=1):
            print(f"{idx}. {theater_name}")
        try:
            theater_idx = input("Enter theater index: (or type 'exit' to cancel): ")
            if theater_idx.lower() == 'exit':
                print("Exiting ticket booking!")
            theater_idx = int(theater_idx) - 1
            if theater_idx < 0:
                raise ValueError
            if theater_idx >= len(theaters):
                raise IndexError
            theater_name = theaters[theater_idx]
        except (ValueError, IndexError):
            print("Invalid input!")
            return

        # Select showtime
        print("\n--- Select a Showtime ---")
        showtimes = movie.get_showtimes(theater_name)
        for idx, showtime in enumerate(showtimes, start=1):
            print(f"{idx}. {showtime}")

        try:
            showtime_idx = input("Enter showtime index: (or type 'exit' to cancel): ")
            showtime_idx = int(showtime_idx) - 1
            if showtime_idx < 0:
                raise ValueError
            if showtime_idx >= len(showtimes):
                raise IndexError
            showtime = showtimes[showtime_idx]
        except (ValueError, IndexError):
            print("Invalid input!")
            return

        # Book seat
        theater = self.theaters[theater_name]
        print(f"\n--- Booking Ticket for {movie_title} ---")

        while True:
            theater.display_seats(showtime)
            try:
                row = input("Enter row number: (or type 'exit' to cancel): ")
                if row.lower() == 'exit':
                    print("Exiting ticket booking!")
                    return
                row = int(row) - 1
                if row < 0 or row >= theater.rows:
                    raise IndexError
                col = input("Enter column letter: (or type 'exit' to cancel): ")
                if col.lower() == 'exit':
                    print("Exiting ticket booking!")
                    return
                col = string.ascii_uppercase.index(col.upper())
                theater.book_seat(row, col, showtime)
                ticket = f"{movie_title} | {theater_name} | {showtime} | Seat ({row + 1}, {chr(col + 65)})"
                self.current_user.add_ticket(ticket)
                print("Ticket booked successfully!")
                break
            except (ValueError, IndexError):
                print("Invalid input! Please try again.")
            except Exception as e:
                print(f"Error: {e}. Please try again.")

    def view_tickets(self):
        if not self.current_user:
            print("Please log in to view your tickets!")
            return

        print(f"--- Tickets for {self.current_user.username} ---")
        if not self.current_user.tickets:
            print("No tickets booked yet!")
        else:
            for ticket in self.current_user.tickets:
                print(ticket)

    def main_menu(self):
        while True:
            print("\n=== Cinema Ticket Booking ===")
            if self.current_user is None:
                print("1. Register")
                print("2. Login")
                print("3. View Movies")
                print("4. Exit")
            else:
                print("1. View Movies")
                print("2. Book Ticket")
                print("3. View My Tickets")
                print("4. Logout")
            choice = input("Select an option: ")

            if self.current_user is None:
                if choice == "1":
                    self.register()
                elif choice == "2":
                    self.login()
                elif choice == "3":
                    self.view_movies()
                elif choice == "4":
                    print("Goodbye!")
                    break
                else:
                    print("Invalid option. Please try again.")
            else:
                if choice == "1":
                    self.view_movies()
                elif choice == "2":
                    self.book_ticket()
                elif choice == "3":
                    self.view_tickets()
                elif choice == "4":
                    self.logout()
                else:
                    print("Invalid option. Please try again.")
