import random

def find_winning_tickets(filename, user_tickets):
    with open(filename, 'r') as file:
        winning_numbers = file.read().strip().split('\n')

    winning_set = set(winning_numbers)
    matched_tickets = [ticket for ticket in user_tickets if ticket in winning_set]
    return matched_tickets