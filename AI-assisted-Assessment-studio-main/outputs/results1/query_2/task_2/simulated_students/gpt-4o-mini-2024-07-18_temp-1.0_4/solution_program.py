import random

def find_winning_tickets(filename, user_tickets):
    with open(filename, 'r') as file:
        winning_numbers = file.read().strip().split('\n')

    winning_tickets = []
    for ticket in user_tickets:
        if ticket in winning_numbers:
            winning_tickets.append(ticket)

    return winning_tickets