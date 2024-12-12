class Seat:
    def __init__(self, row: int, col: int):
        if not isinstance(row, int) or not isinstance(col, int):
            raise ValueError("Row and column must be integers")
        if row < 0 or col < 0:
            raise ValueError("Row and column must be non-negative")
        self.row: int = row
        self.col: int = col
        self.is_booked: bool = False

    def display(self) -> str:
        return "\U0001FA91" if not self.is_booked else "❌"

    def book(self) -> None:
        if self.is_booked:
            raise Exception("Seat already booked!")
        self.is_booked = True

