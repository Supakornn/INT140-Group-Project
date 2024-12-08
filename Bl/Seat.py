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

