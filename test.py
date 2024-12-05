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
        self.seats = [[Seat(r, c) for c in range(cols)] for r in range(rows)]

    def display_seats(self):
        # Display column labels (A, B, C, ...)
        col_labels = list(string.ascii_uppercase[:self.cols])
        print("    " + "  ".join(col_labels))  # Column headers
        for r_idx, row in enumerate(self.seats, start=1):
            # Display each row with its seats and row number
            row_display = " ".join(seat.display() for seat in row)
            print(f"{r_idx:2} {row_display}")  # Row numbers with seat displays

    def book_seat(self, row, col):
        self.seats[row][col].book()


class CinemaApp:
    def __init__(self):
        self.users = {}  # username -> User
        self.current_user = None
        self.theaters = {}  # theater_name -> Theater
        self.load_theaters()

    def load_theaters(self):
        for theater_name, config in MockData.THEATERS.items():
            self.theaters[theater_name] = Theater(config["rows"], config["cols"])

    def register(self, username, password):
        if username == 'exit' or password == 'exit':
            print("Exiting registration!")
            return None, None
        if username in self.users:
            print("Username already exists!")
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

        # Display movies with index
        print("\n--- Select a Movie ---")
        movies = list(MockData.MOVIES.keys())
        for idx, movie in enumerate(movies, start=1):
            print(f"{idx}. {movie}")

        # Select movie by index
        try:
            movie_idx = int(input("Enter movie index (or type 'exit' to cancel): ")) - 1
            if movie_idx == 'exit':
                print("Exiting movie selection!")
                return
            if movie_idx < 0 or movie_idx >= len(movies):
                print("Invalid movie index!")
                return
            movie_title = movies[movie_idx]
        except ValueError:
            print("Invalid input. Please enter a number!")
            return

        # Select theater
        print("\n--- Select a Theater ---")
        theaters = list(MockData.MOVIES[movie_title].keys())
        for idx, theater in enumerate(theaters, start=1):
            print(f"{idx}. {theater}")

        try:
            theater_idx = int(input("Enter theater index (or type 'exit' to cancel): ")) - 1
            if theater_idx == 'exit':
                print("Exiting theater selection!")
                return
            if theater_idx < 0 or theater_idx >= len(theaters):
                print("Invalid theater index!")
                return
            theater_name = theaters[theater_idx]
        except ValueError:
            print("Invalid input. Please enter a number!")
            return

        # Select showtime
        print("\n--- Select a Showtime ---")
        showtimes = MockData.MOVIES[movie_title][theater_name]
        for idx, showtime in enumerate(showtimes, start=1):
            print(f"{idx}. {showtime}")

        try:
            showtime_idx = int(input("Enter showtime index (or type 'exit' to cancel): ")) - 1
            if showtime_idx == 'exit':
                print("Exiting showtime selection!")
                return
            if showtime_idx < 0 or showtime_idx >= len(showtimes):
                print("Invalid showtime index!")
                return
            showtime = showtimes[showtime_idx]
        except ValueError:
            print("Invalid input. Please enter a number!")
            return

        # Book a seat
        try:
            print(f"\n--- Booking Ticket for {movie_title} ---")
            theater = self.theaters[theater_name]
            print(f"--- Seating for {theater_name} ---")
            theater.display_seats()

            # Prompt for row and column selection
            while True:
                # Ask for row and column input together
                while True:
                    row_input = input("Enter row number (or type 'exit' to cancel): ")
                    if row_input.lower() == "exit":
                        print("Booking canceled!")
                        return
                    try:
                        row = int(row_input) - 1
                        if row < 0 or row >= theater.rows:
                            print("Invalid row number! Try again.")
                            continue
                    except ValueError:
                        print("Invalid input. Please enter a valid row number.")
                        continue

                    # Ask for column input
                    col_input = input("Enter column letter (or type 'exit' to cancel): ")
                    if col_input.lower() == "exit":
                        print("Booking canceled!")
                        return
                    col_input = col_input.upper()
                    if col_input not in string.ascii_uppercase[:theater.cols]:
                        print("Invalid column letter! Try again.")
                        continue
                    col = string.ascii_uppercase.index(col_input)

                    # Check if the seat is already booked
                    if theater.seats[row][col].is_booked:
                        print("Seat is already booked! Please choose a different seat.")
                        continue  # Ask the user for a new row and column
                    break  # Exit the loop if the seat is available

                # Book the seat
                theater.book_seat(row, col)
                ticket = f"{movie_title} | {theater_name} | {showtime} | Seat ({row + 1},{col_input})"
                self.current_user.add_ticket(ticket)
                print("Ticket booked successfully!")
                break  # Exit the while loop after booking successfully

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
            print("1. Register")
            print("2. Login")
            print("3. View Movies")
            print("4. Book Ticket")
            print("5. View My Tickets")
            print("6. Exit")
            choice = input("Select an option: ")

            if choice == "1":
                username = input("Enter username (or type 'exit' to cancel): ")
                password = input("Enter password (or type 'exit' to cancel): ")
                if username == 'exit' or password == 'exit':
                    print("Exiting registration!")
                    continue
                self.register(username, password)
            elif choice == "2":
                self.login()
            elif choice == "3":
                self.view_movies()
            elif choice == "4":
                self.book_ticket()
            elif choice == "5":
                self.view_tickets()
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")


if __name__ == "__main__":
    app = CinemaApp()
    app.main_menu()
