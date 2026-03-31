import os

def find_winning_tickets(filename, user_tickets):
    # Read winning numbers from file
    with open(filename, 'r') as file:
        winning_sets = file.read().splitlines()
    
    # Initialize result list
    matching_tickets = []

    # Check each user ticket against the winning numbers
    for ticket in user_tickets:
        if ticket in winning_sets:
            matching_tickets.append(ticket)

    return matching_tickets