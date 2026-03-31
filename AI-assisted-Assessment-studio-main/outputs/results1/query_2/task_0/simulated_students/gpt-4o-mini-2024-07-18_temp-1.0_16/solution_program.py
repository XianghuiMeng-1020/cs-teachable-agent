import random

def get_lucky_winner(file_path):
    with open(file_path, 'r') as file:
        tickets = file.readlines()
        participants = []
        total_length = 0
        
        for ticket in tickets:
            name, ticket_number = ticket.strip().split(':')
            participants.append((name, ticket_number))
            total_length += len(ticket_number)
        
        if total_length == 0:
            return None
        
        stopping_position = total_length % len(participants)
        winner_index = stopping_position % len(participants)
        
        return participants[winner_index][0]