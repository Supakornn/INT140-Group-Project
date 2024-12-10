import string
from Bl.Seat import Seat

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
        return [
            [seat.display() for seat in row] for row in self.showtime_seating[showtime]
        ]
        
    def book_seat(self, row, col, showtime):
        if showtime not in self.showtime_seating:
            raise Exception("Invalid showtime!")
        self.showtime_seating[showtime][row][col].book()
