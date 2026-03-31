import random

def find_winning_tickets(filename, user_tickets):
    with open(filename, 'r') as file:
        winning_sets = file.read().strip().split('\n')
    winning_sets = set(winning_sets)

    matching_tickets = []
    for ticket in user_tickets:
        if ticket in winning_sets:
            matching_tickets.append(ticket)
    return matching_tickets