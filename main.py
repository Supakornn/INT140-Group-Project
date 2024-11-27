from Cinema import Cinema
from Theater import Theater
from Movie import Movie
from Booking import Booking

cinema = Cinema("Mega Cinema")

theater1 = Theater(1, "Theater One", seats_per_row=5, rows=5)
cinema.add_theater(theater1)

movie1 = Movie("Avengers", "19:00")
theater1.add_movie(movie1)

cinema.show_theaters()

print("\nSeats before booking:")
theater1.show_seats()

seat_to_book = theater1.seats[1][0] 
booking1 = Booking("Gap", seat_to_book)
movie1.add_booking(booking1)

print("\nSeats after booking:")
theater1.show_seats()

movie1.show_bookings()
