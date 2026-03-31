import random

def find_winning_tickets(filename, user_tickets):
    with open(filename, 'r') as file:
        winning_sets = file.read().strip().split('\n')
    winning_sets = set(winning_sets)  # Use a set for faster lookup
    matching_tickets = [ticket for ticket in user_tickets if ticket in winning_sets]
    return matching_tickets