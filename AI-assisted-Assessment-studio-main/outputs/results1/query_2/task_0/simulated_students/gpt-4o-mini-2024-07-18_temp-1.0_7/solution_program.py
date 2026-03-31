import random

def get_lucky_winner(file_path):
    ticket_info = {}
    total_length = 0

    with open(file_path, 'r') as file:
        for line in file:
            name, ticket = line.strip().split(':')
            ticket_info[name] = ticket
            total_length += len(ticket)

    tickets = list(ticket_info.values())
    positions = [(i + 1) * len(tickets) for i in range(len(tickets))]

    stopping_position = total_length % len(tickets)
    winner_index = stopping_position if stopping_position != 0 else len(tickets) - 1

    winner_name = list(ticket_info.keys())[winner_index]
    return winner_name