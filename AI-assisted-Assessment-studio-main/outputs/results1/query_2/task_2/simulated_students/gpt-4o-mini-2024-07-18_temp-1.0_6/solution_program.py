import random

def find_winning_tickets(filename, user_tickets):
    with open(filename, 'r') as file:
        winning_numbers = file.read().strip().split('\n')

    winning_set = set()
    for numbers in winning_numbers:
        winning_set.add(frozenset(numbers.split()))

    matching_tickets = []
    for ticket in user_tickets:
        if frozenset(ticket.split()) in winning_set:
            matching_tickets.append(ticket)

    return matching_tickets