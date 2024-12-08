import string

# Mockup Data
class MockData:
    CINEMA_NAME = "MyCinema"
    MOVIES = {
        "Avatar": {
            "Theater 1": ["10:00", "14:00"],
            "Theater 2": ["18:00"],
        },
        "Titanic": {
            "Theater 1": ["12:00", "16:00"],
            "Theater 2": ["20:00"],
        },
    }
    THEATERS = {
        "Theater 1": {"rows": 5, "cols": 5},
        "Theater 2": {"rows": 4, "cols": 6},
    }


# Business Logic
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.tickets = []  # List of tickets booked by the user

    def add_ticket(self, ticket):
        self.tickets.append(ticket)


class Seat:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_booked = False

    def display(self):
        return "\U0001FA91" if not self.is_booked else "❌"

    def book(self):
        if self.is_booked:
            raise Exception("Seat already booked!")
        self.is_booked = True


class Theater:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.showtime_seating = {}  # Maps showtime to seating arrangement

    def setup_showtimes(self, showtimes):
        for showtime in showtimes:
            self.showtime_seating[showtime] = [
                [Seat(r, c) for c in range(self.cols)] for r in range(self.rows)
            ]

    def display_seats(self, showtime):
        if showtime not in self.showtime_seating:
            print("Showtime not found!")
            return
        col_labels = list(string.ascii_uppercase[:self.cols])
        print("    " + "  ".join(col_labels))  # Print column headers
        for r_idx, row in enumerate(self.showtime_seating[showtime], start=1):
            row_display = " ".join(seat.display() for seat in row)
            print(f"{r_idx:2} {row_display}")

    def book_seat(self, row, col, showtime):
        if showtime not in self.showtime_seating:
            raise Exception("Invalid showtime!")
        self.showtime_seating[showtime][row][col].book()


class Movie:
    def __init__(self, title):
        self.title = title
        self.theaters = {}  # theater_name -> list of showtimes

    def add_showtime(self, theater_name, showtimes):
        self.theaters[theater_name] = showtimes

    def get_theaters(self):
        return self.theaters.keys()

    def get_showtimes(self, theater_name):
        return self.theaters.get(theater_name, [])


class CinemaApp:
    def __init__(self):
        self.users = {}  # username -> User
        self.current_user = None
        self.theaters = {}  # theater_name -> Theater
        self.movies = {}  # movie_title -> Movie
        self.load_theaters()
        self.load_movies()

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

        # Display movies
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


if __name__ == "__main__":
    app = CinemaApp()
    app.main_menu()
