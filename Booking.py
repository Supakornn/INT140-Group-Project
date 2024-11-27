class Booking:
    def __init__(self, customer_name, seat):
        self.customer_name = customer_name
        self.seat = seat
        self.seat.reserve()
