class Movie:
    def __init__(self, title):
        self.title = title
        self.theaters = {}  # theater -> showtimes

    def add_showtime(self, theater_name, showtimes):
        self.theaters[theater_name] = showtimes

    def get_theaters(self):
        return self.theaters.keys()

    def get_showtimes(self, theater_name):
        return self.theaters.get(theater_name, [])
