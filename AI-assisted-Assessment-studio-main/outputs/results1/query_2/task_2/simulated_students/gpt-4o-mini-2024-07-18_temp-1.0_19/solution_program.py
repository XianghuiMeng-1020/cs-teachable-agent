import random

def find_winning_tickets(filename, user_tickets):
    with open(filename, 'r') as file:
        winning_sets = [line.strip() for line in file.readlines()]

    winning_tickets = []
    for ticket in user_tickets:
        if ticket in winning_sets:
            winning_tickets.append(ticket)

    return winning_tickets