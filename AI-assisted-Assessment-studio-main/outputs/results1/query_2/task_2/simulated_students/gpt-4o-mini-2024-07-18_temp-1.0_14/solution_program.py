import random

def find_winning_tickets(filename, user_tickets):
    with open(filename, 'r') as file:
        winning_sets = [line.strip() for line in file.readlines()]
    winning_numbers = set(tuple(map(int, winning_set.split())) for winning_set in winning_sets)
    matching_tickets = []
    for ticket in user_tickets:
        ticket_numbers = set(map(int, ticket.split()))
        if ticket_numbers in winning_numbers:
            matching_tickets.append(ticket)
    return matching_tickets