from typing import List, Dict

class Movie:
    def __init__(self, title: str):
        if not title:
            raise ValueError("Title cannot be empty.")
        self.title: str = title
        self.theaters: Dict[str, List[str]] = {}  # theater -> showtimes

    def add_showtime(self, theater_name: str, showtimes: List[str]) -> None:
        if not theater_name or not showtimes:
            raise ValueError("Theater name and showtimes cannot be empty.")
        for showtime in showtimes:
            if not isinstance(showtime, str) or not showtime.strip():
                raise ValueError("Invalid showtime.")
        self.theaters[theater_name] = showtimes

    def get_theaters(self) -> List[str]:
        return list(self.theaters.keys())

    def get_showtimes(self, theater_name: str) -> List[str]:
        return self.theaters.get(theater_name, [])
