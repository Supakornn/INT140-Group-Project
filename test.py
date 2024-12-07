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
        # Display emoji based on seat booking status
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
        for showtime in MockData.MOVIES.values():
            for theater_showtime in showtime.values():
                for time in theater_showtime:
                    self.showtime_seating[time] = [
                        [Seat(r, c) for c in range(cols)] for r in range(rows)
                    ]

    def display_seats(self, showtime):
        # Display column labels (A, B, C, ...)
        if showtime not in self.showtime_seating:
            print("Showtime not found!")
            return
        col_labels = list(string.ascii_uppercase[:self.cols])
        print("    " + "  ".join(col_labels))  # Print column headers
        for r_idx, row in enumerate(self.showtime_seating[showtime], start=1):
            # Display each row with its seats and row number
            row_display = " ".join(seat.display() for seat in row)
            print(f"{r_idx:2} {row_display}")  # Print row number with seat displays

    def book_seat(self, row, col, showtime):
        if showtime not in self.showtime_seating:
            raise Exception("Invalid showtime!")
        self.showtime_seating[showtime][row][col].book()


class CinemaApp:
    def __init__(self):
        self.users = {}  # username -> User
        self.current_user = None
        self.theaters = {}  # theater_name -> Theater
        self.load_theaters()

    def load_theaters(self):
        for theater_name, config in MockData.THEATERS.items():
            self.theaters[theater_name] = Theater(config["rows"], config["cols"])

    def register(self):
        while True:
            username = input("Enter username (or type 'exit' to cancel): ")
            if username.lower() == 'exit':
                print("Exiting registration!")
                return None, None
            if username in self.users:
                print("Username already exists! Please try again.")
                continue
            password = input("Enter password (or type 'exit' to cancel): ")
            if password.lower() == 'exit':
                print("Exiting registration!")
                return None, None
            self.users[username] = User(username, password)
            print("User registered successfully!")
            return username, password


    def login(self):
        while True:
            username = input("Enter username (or type 'exit' to cancel): ")
            if username == 'exit':
                print("Exiting login!")
                return None
            if username not in self.users:
                print("Username not found. Please try again.")
                continue
            password = input("Enter password (or type 'exit' to cancel): ")
            if password == 'exit':
                print("Exiting login!")
                return None
            if self.users[username].password != password:
                print("Incorrect password. Please try again.")
                continue
            self.current_user = self.users[username]
            print(f"Welcome, {username}!")
            break

    def logout(self):
        self.current_user = None
        print(f"Logout success!")

    def view_movies(self):
        print(f"--- Movies in {MockData.CINEMA_NAME} ---")
        for idx, (movie, theaters) in enumerate(MockData.MOVIES.items(), start=1):
            print(f"{idx}. {movie}:")
            for theater, showtimes in theaters.items():
                print(f"  {theater}: {', '.join(showtimes)}")

    def book_ticket(self):
        if not self.current_user:
            print("Please log in to book a ticket!")
            return

        # Display movies
        print("\n--- Select a Movie ---")
        movies = list(MockData.MOVIES.keys())
        for idx, movie in enumerate(movies, start=1):
            print(f"{idx}. {movie}")

        try:
            movie_idx = int(input("Enter movie index (or type 'exit' to cancel): ")) - 1
            if movie_idx == 'exit':
                print("Exiting booking!")
                return
            movie_title = movies[movie_idx]
        except (ValueError, IndexError):
            print("Invalid input!")
            return

        # Select theater
        print("\n--- Select a Theater ---")
        theaters = list(MockData.MOVIES[movie_title].keys())
        for idx, theater in enumerate(theaters, start=1):
            print(f"{idx}. {theater}")

        try:
            theater_idx = int(input("Enter theater index (or type 'exit' to cancel): ")) - 1
            if theater_idx == 'exit':
                print("Exiting booking!")
                return
            theater_name = theaters[theater_idx]
        except (ValueError, IndexError):
            print("Invalid input!")
            return

        # Select showtime
        print("\n--- Select a Showtime ---")
        showtimes = MockData.MOVIES[movie_title][theater_name]
        for idx, showtime in enumerate(showtimes, start=1):
            print(f"{idx}. {showtime}")

        try:
            showtime_idx = int(input("Enter showtime index (or type 'exit' to cancel): ")) - 1
            if showtime_idx == 'exit':
                print("Exiting booking!")
                return
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
                row_input = input("Enter row number (or type 'exit' to cancel): ")
                if row_input.lower() == 'exit':
                    print("Exiting booking!")
                    return
                row = int(row_input) - 1
                col_input = input("Enter column letter (or type 'exit' to cancel): ").upper()
                if col_input.lower() == 'exit':
                    print("Exiting booking!")
                    return
                col = string.ascii_uppercase.index(col_input)
                theater.book_seat(row, col, showtime)
                ticket = f"{movie_title} | {theater_name} | {showtime} | Seat ({row + 1},{chr(col + 65)})"
                self.current_user.add_ticket(ticket)
                print("Ticket booked successfully!")
                break
            except ValueError:
                print("Invalid row or column input. Please try again.")
            except IndexError:
                print("Invalid seat coordinates. Please try again.")
            except Exception as e:
                print(f"Error: {e}. Please try a different seat.")


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
