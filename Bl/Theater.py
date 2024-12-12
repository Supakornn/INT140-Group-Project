from typing import List, Dict
import string
from Bl.Seat import Seat

class Theater:
    def __init__(self, rows: int, cols: int):
        self.rows: int = rows
        self.cols: int = cols
        self.showtime_seating: Dict[str, List[List[Seat]]] = {}  

    def setup_showtimes(self, showtimes: List[str]) -> None:
        for showtime in showtimes:
            self.showtime_seating[showtime] = [
                [Seat(r, c) for c in range(self.cols)] for r in range(self.rows)
            ]

    def display_seats(self, showtime: str) -> List[str]:
        if showtime not in self.showtime_seating:
            raise Exception("Showtime not found!")
        col_labels = list(string.ascii_uppercase[:self.cols])
        screen_line = "SCREEN".center(self.cols * 3 + 3)
        seat_display = [""]
        seat_display.append(screen_line) # screen line
        seat_display.append("   " + "  ".join(col_labels)) # header column labels (A, B, C, ...)
        for r_idx, row in enumerate(self.showtime_seating[showtime], start=1):
            row_display = " ".join(seat.display() for seat in row) 
            seat_display.append(f"{r_idx} {row_display}")
        return seat_display

    def book_seat(self, row: int, col: int, showtime: str) -> None:
        if showtime not in self.showtime_seating:
            raise Exception("Invalid showtime!")
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            raise ValueError("Invalid seat position.")
        self.showtime_seating[showtime][row][col].book()
