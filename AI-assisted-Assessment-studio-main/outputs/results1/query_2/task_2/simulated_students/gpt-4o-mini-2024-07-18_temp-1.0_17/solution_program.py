import random

def find_winning_tickets(filename, user_tickets):
    with open(filename, 'r') as file:
        winning_numbers = [line.strip() for line in file.readlines()] 

    winning_set = set()  
    for numbers in winning_numbers:
        winning_set.add(numbers)

    matched_tickets = []
    for ticket in user_tickets:
        if ticket in winning_set:
            matched_tickets.append(ticket)

    return matched_tickets