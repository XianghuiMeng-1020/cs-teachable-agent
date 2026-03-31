import random

def find_winning_tickets(filename, user_tickets):
    with open(filename, 'r') as file:
        winning_numbers = {line.strip() for line in file}  # Read all winning sets into a set
    matching_tickets = [ticket for ticket in user_tickets if ticket in winning_numbers]
    return matching_tickets