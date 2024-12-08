class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.tickets = []  #User Tickets

    def add_ticket(self, ticket):
        self.tickets.append(ticket)
