# Cinema Booking System

## Project Structure

```
INT140-Group-Project/
│
├── Bl/
│   ├── CinemaBl.py
│   ├── MockData.py
│   ├── Movie.py
│   ├── Seat.py
│   ├── Theater.py
│   ├── User.py
│   └── UserManager.py
│
├── Ui/
│   └── CinemaUI.py
│
└── main.py
```

## Classes and Attributes

### CinemaBl

- **Attributes:**
  - `theaters: Dict[str, Theater]`
  - `movies: Dict[str, Movie]`
- **Methods:**
  - `__init__()`
  - `load_theaters()`
  - `load_movies()`
  - `_validate_theater_data(theater_name: str, config: dict)`
  - `_validate_movie_data(movie_title: str, theaters: dict)`
  - `_setup_movie_showtimes(movie: Movie, theaters: dict)`
  - `get_movies() -> Dict[str, Movie]`
  - `get_theaters() -> Dict[str, Theater]`
  - `display_user_tickets(user: User)`

### UserManager

- **Attributes:**
  - `users: Dict[str, User]`
  - `current_user: Optional[User]`
- **Methods:**
  - `__init__()`
  - `register(username: str, password: str)`
  - `login(username: str, password: str)`
  - `logout()`
  - `book_ticket(movie_title: str, theater_name: str, showtime: str, row: int, col: int, cinema_bl: CinemaBl)`
  - `_validate_credentials(username: str, password: str)`
  - `_validate_booking(movie_title: str, theater_name: str, showtime: str, row: int, col: int, cinema_bl: CinemaBl)`

### User

- **Attributes:**
  - `username: str`
  - `password: str`
  - `tickets: List[Dict[str, str]]`
- **Methods:**
  - `__init__(username: str, password: str)`
  - `add_ticket(ticket: Dict[str, str])`
  - `view_tickets() -> List[str]`

### Theater

- **Attributes:**
  - `rows: int`
  - `cols: int`
  - `showtime_seating: Dict[str, List[List[Seat]]]`
- **Methods:**
  - `__init__(rows: int, cols: int)`
  - `setup_showtimes(showtimes: List[str])`
  - `display_seats(showtime: str) -> List[str]`
  - `book_seat(row: int, col: int, showtime: str)`

### Seat

- **Attributes:**
  - `row: int`
  - `col: int`
  - `is_booked: bool`
- **Methods:**
  - `__init__(row: int, col: int)`
  - `display() -> str`
  - `book()`
  - `_validate_position(row: int, col: int)`

### Movie

- **Attributes:**
  - `title: str`
  - `theaters: Dict[str, List[str]]`
- **Methods:**
  - `__init__(title: str)`
  - `add_showtime(theater_name: str, showtimes: List[str])`
  - `get_theaters() -> List[str]`
  - `get_showtimes(theater_name: str) -> List[str]`
  - `_validate_title(title: str)`
  - `_validate_showtime_data(theater_name: str, showtimes: List[str])`

### MockData

- **Attributes:**
  - `CINEMA_NAME: str`
  - `MOVIES: Dict[str, Dict[str, List[str]]]`
  - `THEATERS: Dict[str, Dict[str, int]]`

## Logic of Methods

### CinemaBl

- **load_theaters()**: Loads theater data from `MockData` and initializes `Theater` objects.
- **load_movies()**: Loads movie data from `MockData` and initializes `Movie` objects, setting up showtimes in theaters.
- **\_validate_theater_data()**: Validates theater data.
- **\_validate_movie_data()**: Validates movie data.
- **\_setup_movie_showtimes()**: Sets up showtimes for movies in theaters.
- **get_movies()**: Returns the dictionary of movies.
- **get_theaters()**: Returns the dictionary of theaters.
- **display_user_tickets()**: Displays the tickets of a user.

### UserManager

- **register()**: Registers a new user.
- **login()**: Logs in an existing user.
- **logout()**: Logs out the current user.
- **book_ticket()**: Books a ticket for the current user.
- **\_validate_credentials()**: Validates user credentials.
- **\_validate_booking()**: Validates booking details.

### User

- **add_ticket()**: Adds a ticket to the user's list.
- **view_tickets()**: Returns a list of the user's tickets.

### Theater

- **setup_showtimes()**: Sets up showtimes for the theater.
- **display_seats()**: Displays the seating arrangement for a showtime.
- **book_seat()**: Books a seat for a showtime.

### Seat

- **display()**: Returns the display character for the seat.
- **book()**: Books the seat.
- **\_validate_position()**: Validates the seat position.

### Movie

- **add_showtime()**: Adds showtimes for a theater.
- **get_theaters()**: Returns the list of theaters showing the movie.
- **get_showtimes()**: Returns the list of showtimes for a theater.
- **\_validate_title()**: Validates the movie title.
- **\_validate_showtime_data()**: Validates showtime data.

## User Flow

1. **Main Menu**: The user starts at the main menu provided by `CinemaUI`.
2. **Registration/Login**: The user can register a new account or log in to an existing account using `UserManager`.
3. **View Movies**: The user can view the list of available movies and their showtimes.
4. **Book Tickets**: The user can book tickets for a movie by selecting the movie, theater, showtime, and seat.
5. **View Tickets**: The user can view their booked tickets.
6. **Logout**: The user can log out of their account.
