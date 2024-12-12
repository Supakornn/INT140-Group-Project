from Bl.CinemaBl import CinemaBl
from Bl.UserManager import UserManager
import string

class CinemaUI:
    def __init__(self):
        self.user_manager: UserManager = UserManager()
        self.cinema_bl: CinemaBl = CinemaBl()

    def register(self) -> None:
        err_count = 0
        while err_count < 5:
            username: str = input("Enter username (or type 'exit' to cancel): ")
            if username.lower() == 'exit':
                print("Exiting registration!")
                return
            password: str = input("Enter password: (or type 'exit' to cancel): ")
            if password.lower() == 'exit':
                print("Exiting registration!")
                return
            try:
                self.user_manager.register(username, password)
                print("User registered successfully!")
                return
            except ValueError as e:
                err_count += 1
                print(e)
        else:
            print("Too many failed registration. Exiting registration!")

    def login(self) -> None:
        err_count = 0
        while err_count < 5:
            username: str = input("Enter username (or type 'exit' to cancel): ")
            if username.lower() == 'exit':
                print("Exiting login!")
                return
            password: str = input("Enter password: (or type 'exit' to cancel): ")
            if password.lower() == 'exit':
                print("Exiting login!")
                return
            try:
                self.user_manager.login(username, password)
                print(f"Welcome, {username}!")
                break
            except ValueError as e:
                print(e)
                err_count += 1
        else:
            print("Too many failed login. Exiting login!")

    def logout(self) -> None:
        self.user_manager.logout()
        print("Logout success!")

    def book_ticket(self) -> None:
        if not self.user_manager.current_user:
            print("Please log in to book a ticket!")
            return

        # Select Movie
        movie_err_count = 0
        while movie_err_count < 5:
            try:
                print("\n--- Select a Movie ---")
                movies: dict = self.cinema_bl.get_movies()
                movie_titles: list = list(movies.keys())
                for idx, movie_title in enumerate(movie_titles, start=1):
                    print(f"{idx}. {movie_title}")

                movie_idx: str = input("Enter movie index: (or type 'exit' to cancel): ")
                if movie_idx.lower() == 'exit':
                    print("Exiting ticket booking!")
                    return
                if not movie_idx.isdigit():
                    raise ValueError("Invalid movie index!")
                movie_idx: int = int(movie_idx) - 1
                if movie_idx < 0 or movie_idx >= len(movie_titles):
                    raise ValueError("Invalid movie index!")
                movie_title: str = movie_titles[movie_idx]
                break
            except ValueError as e:
                print(e)
                movie_err_count += 1
        else:
            print("Too many failed attempts. Exiting ticket booking!")
            return

        movie = movies[movie_title]

        # Select theater
        theater_err_count = 0
        while theater_err_count < 5:
            try:
                print("\n--- Select a Theater ---")
                theaters: list = list(movie.get_theaters())
                for idx, theater_name in enumerate(theaters, start=1):
                    print(f"{idx}. {theater_name}")

                theater_idx: str = input("Enter theater index: (or type 'exit' to cancel): ")
                if theater_idx.lower() == 'exit':
                    print("Exiting ticket booking!")
                    return
                if not theater_idx.isdigit():
                    raise ValueError("Invalid theater index!")
                theater_idx: int = int(theater_idx) - 1
                if theater_idx < 0 or theater_idx >= len(theaters):
                    raise ValueError("Invalid theater index!")
                theater_name: str = theaters[theater_idx]
                break
            except ValueError as e:
                print(e)
                theater_err_count += 1
        else:
            print("Too many failed attempts. Exiting ticket booking!")
            return

        # Select showtime
        showtime_err_count = 0
        while showtime_err_count < 5:
            try:
                print("\n--- Select a Showtime ---")
                showtimes: list = movie.get_showtimes(theater_name)
                for idx, showtime in enumerate(showtimes, start=1):
                    print(f"{idx}. {showtime}")

                showtime_idx: str = input("Enter showtime index: (or type 'exit' to cancel): ")
                if showtime_idx.lower() == 'exit':
                    print("Exiting ticket booking!")
                    return
                if not showtime_idx.isdigit():
                    raise ValueError("Invalid showtime index!")
                showtime_idx: int = int(showtime_idx) - 1
                if showtime_idx < 0 or showtime_idx >= len(showtimes):
                    raise ValueError("Invalid showtime index!")
                showtime: str = showtimes[showtime_idx]
                break
            except ValueError as e:
                print(e)
                showtime_err_count += 1
        else:
            print("Too many failed attempts. Exiting ticket booking!")
            return

        # Book seat
        theater = self.cinema_bl.get_theaters()[theater_name]
        print(f"\n--- Booking Ticket for {movie_title} ---")
        seat_err_count = 0
        while seat_err_count < 5:
            try:
                seat_display: list = theater.display_seats(showtime)
                for line in seat_display:
                    print(line)
                row: str = input(f"Enter row number: (or type 'exit' to cancel): ")
                if row.lower() == 'exit':
                    print("Exiting ticket bookingå!")
                    return
                if not row.isdigit() or int(row) < 1 or int(row) > theater.rows:
                    raise ValueError("Invalid row number!")
                row: int = int(row) - 1

                col: str = input("Enter column letter: (or type 'exit' to cancel): ")
                if col.lower() == 'exit':
                    print("Exiting ticket booking!")
                    return
                if col.upper() not in string.ascii_uppercase[:theater.cols]:
                    raise ValueError("Invalid column letter!")
                col: int = string.ascii_uppercase.index(col.upper())

                self.user_manager.book_ticket(movie_title, theater_name, showtime, row, col, self.cinema_bl)
                print("Ticket booked successfully!")
                return
            except ValueError as e:
                print(e)
                seat_err_count += 1
            except Exception as e:
                print(f"{e} Please try again.")
                seat_err_count += 1
        print("Too many failed attempts. Exiting ticket booking!")

    def view_tickets(self) -> None:
        if not self.user_manager.current_user:
            print("Please log in to view your tickets!")
            return

        print(f"--- Tickets for {self.user_manager.current_user.username} ---")
        tickets = self.user_manager.current_user.view_tickets()
        if not tickets:
            print("No tickets booked yet!")
        else:
            for ticket in tickets:
                print(ticket)

    def view_movies(self) -> None:
        print("\n--- Movies in Cinema ---")
        movies: dict = self.cinema_bl.get_movies()
        for idx, (movie_title, movie) in enumerate(movies.items(), start=1):
            print(f"{idx}. {movie_title}:")
            for theater_name, showtimes in movie.theaters.items():
                print(f"  {theater_name}: {', '.join(showtimes)}")

    def main_menu(self) -> None:
        while True:
            print("\n=== Cinema Ticket Booking ===")
            if self.user_manager.current_user is None:
                print("1. Register")
                print("2. Login")
                print("3. View Movies")
                print("4. Exit")
            else:
                print("1. View Movies")
                print("2. Book Ticket")
                print("3. View My Tickets")
                print("4. Logout")
            choice: str = input("Select an option: ")

            if self.user_manager.current_user is None:
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
