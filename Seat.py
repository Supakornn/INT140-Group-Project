class Seat:
    def __init__(self, row, number):
        self.row = row
        self.number = number
        self.is_reserved = False

    @property
    def status(self):            
        return "❌" if self.is_reserved else "\U0001FA91"

    def reserve(self):
        if not self.is_reserved:
            self.is_reserved = True
            print(f"Seat {self.row}-{self.number} reserved.")
        else:
            print(f"Seat {self.row}-{self.number} is already reserved.")
