import random

def find_winning_tickets(filename, user_tickets):
    with open(filename, 'r') as file:
        winning_numbers = [line.strip() for line in file.readlines()]

    winning_set = random.choice(winning_numbers)

    return [ticket for ticket in user_tickets if ticket == winning_set]