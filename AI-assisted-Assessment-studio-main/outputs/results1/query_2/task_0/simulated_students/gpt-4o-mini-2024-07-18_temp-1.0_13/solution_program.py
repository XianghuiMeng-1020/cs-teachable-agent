import random

def get_lucky_winner(file_path):
    with open(file_path, 'r') as file:
        tickets = {}
        total_length = 0
        for line in file:
            name, ticket_number = line.strip().split(':')
            tickets[ticket_number] = name
            total_length += len(ticket_number)

    position = total_length % len(tickets)
    ticket_list = list(tickets.keys())
    winner_ticket = ticket_list[position]  
    return tickets[winner_ticket]