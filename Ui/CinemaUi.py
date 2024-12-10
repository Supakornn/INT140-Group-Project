import string
from Bl.CinemaBl import CinemaBl

class CinemaUi:
    def __init__(self):
        self.cinemaBl = CinemaBl()
    def register(self):
        err_count = 0
        while True:
            try:
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
                self.CinemaBl.register(username, password)
                print("User registered successfully!")
                return
            except Exception as e:
                print(e)
                err_count += 1
                if err_count >= 3:
                    print("Too many errors! Exiting registration.")
                    err_count = 0
                    return

    def login(self):
        err_count = 0
        while True:
            try:
                username = input("Enter username (or type 'exit' to cancel): ")
                if username.lower() == 'exit':
                    print("Exiting login!")
                    return
                password = input("Enter password: (or type 'exit' to cancel): ")
                if password.lower() == 'exit':
                    print("Exiting login!")
                    return
                user = self.CinemaBl.login(username, password)
                print(f"Welcome, {user}!")
                break
            except Exception as e:
                print(e)
                err_count += 1
                if err_count >= 3:
                    print("Too many errors! Exiting login.")
                    err_count = 0
                    return

    def logout(self):
        self.cinemaBl.logout()
        print("Logout success!")

    def view_movies(self):
        print("\n--- Movies in Cinema ---")
        movies = self.cinemaBl.get_movie()
        for movie_title, movie in movies.items():
            print(f"{movie_title}:")
            for theater_name, showtimes in movie.get_theaters().items():
                print(f"  {theater_name}: {', '.join(showtimes)}")

    def book_ticket(self): 
        movie = None
        theater = None
        showtime = None
        
        while True:
            print("\n--- Select a Movie ---")
            movie_titles = self.cinemaBl.get_all_movie()
            for idx, movie_title in enumerate(movie_titles, start=1):
                print(f"{idx}. {movie_title}")
            while True:
                try:
                    movie_idx = input("Enter movie index: (or type 'exit' to cancel): ")
                    if movie_idx.lower() == 'exit':
                        print("Exiting ticket booking!")
                        return
                    movie = self.cinemaBl.get_movie(movie_idx)
                    break
                except Exception as e:
                    print(e)

            print("\n--- Select a Theater ---")
            theaters = self.cinemaBl.get_theaters_for_movie(movie)
            for idx, theater_name in enumerate(theaters, start=1):
                print(f"{idx}. {theater_name}")
            while True:
                try:
                    theater_idx = input("Enter theater index: (or type 'exit' to cancel): ")
                    if theater_idx.lower() == 'exit':
                        print("Exiting ticket booking!")
                        return
                    theater = self.cinemaBl.get_theater(movie,theater_idx)
                    break
                except Exception as e:
                    print(e)

            print("\n--- Select a Showtime ---")
            showtimes = self.cinemaBl.get_showtimes_for_theater(movie,theater)
            for idx, showtime in enumerate(showtimes, start=1):
                print(f"{idx}. {showtime}")
            while True:
                try:
                    showtime_idx = input("Enter showtime index: (or type 'exit' to cancel): ")
                    if showtime_idx.lower() == 'exit':
                        print("Exiting ticket booking!")
                        return
                    showtime = self.CinemaBl.get_showtime(movie,theater,showtime_idx)
                    break
                except Exception as e:
                    print(e)

            print(f"\n--- Booking Ticket for {movie_title} ---")
            col_labels = list(string.ascii_uppercase[:self.cols])
            print("    " + "  ".join(col_labels))
            for r_idx, row_display in enumerate(self.cinemaBl.display_seats(theater,showtime), start=1):
                print(f"{r_idx:2}  " + "  ".join(row_display))
            while True:
                try:
                    row = input("Enter row number: (or type 'exit' to cancel): ")
                    if row.lower() == 'exit':
                        print("Exiting ticket booking!")
                        return
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
                except Exception as e:
                    print(e)

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

            if self.cinemaBl.get_current_user() is None:
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


