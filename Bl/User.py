from typing import List, Dict

class User:
    def __init__(self, username: str, password: str):
        self.username: str = username
        self.password: str = password
        self.tickets: List[Dict[str, str]] = []

    def add_ticket(self, ticket: Dict[str, str]) -> None:
        if not ticket:
            raise ValueError("Ticket information cannot be empty.")
        self.tickets.append(ticket)

    def view_tickets(self) -> List[str]:
        return [
            f"Movie: {ticket['movie']}, Theater: {ticket['theater']}, Showtime: {ticket['showtime']}, Seat: {ticket['row']+1}:{chr(ticket['col']+65)}"
            for ticket in self.tickets
        ]
