class Cinema:
    def __init__(self, name):
        self.name = name
        self.theaters = []
    
    def add_theater(self, theater):
        self.theaters.append(theater)

    def show_theaters(self):
        for theater in self.theaters:
            print(f"Theater {theater.theater_id}: {theater.name}")
