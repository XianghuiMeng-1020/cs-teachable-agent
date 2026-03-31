import random

def find_winning_tickets(filename, user_tickets):
    with open(filename, 'r') as file:
        winning_numbers = [line.strip() for line in file.readlines()]
    matching_tickets = []
    for ticket in user_tickets:
        if ticket in winning_numbers:
            matching_tickets.append(ticket)
    return matching_tickets