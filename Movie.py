class Movie:
    def __init__(self, movie_name, time):
        self.movie_name = movie_name
        self.time = time
        self.bookings = [] 
    
    def add_booking(self, booking):
        self.bookings.append(booking)

    def show_bookings(self):
        print(f"Bookings for {self.movie_name} at {self.time}:")
        for booking in self.bookings:
            print(f"- {booking.customer_name} reserved seat {booking.seat.row}-{booking.seat.number}")
            
