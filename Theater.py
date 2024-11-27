from Seat import Seat

class Theater:
    def __init__(self, theater_id, name, seats_per_row, rows):
        self.theater_id = theater_id
        self.name = name
        self.seats = self._generate_seats(seats_per_row, rows)
        self.showtimes = []
    
    def _generate_seats(self, seats_per_row, rows):
        return [[Seat(row, seat) for seat in range(1, seats_per_row + 1)] for row in range(1, rows + 1)]
    
    def add_showtime(self, showtime):
        self.showtimes.append(showtime)
        
    def show_seats(self):
        header = "  " + "  ".join(chr(65 + i) for i in range(len(self.seats[0])))
        print(header)
        for i, row in enumerate(self.seats):
            row_status = f"{i + 1} " + " ".join(seat.status for seat in row)
            print(row_status)
    
