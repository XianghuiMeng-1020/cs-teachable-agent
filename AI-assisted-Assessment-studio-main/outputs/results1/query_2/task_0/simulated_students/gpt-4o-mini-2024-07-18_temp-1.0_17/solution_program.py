import random

def get_lucky_winner(file_path):
    try:
        with open(file_path, 'r') as file:
            tickets = []
            total_characters = 0
            for line in file:
                name, ticket_number = line.strip().split(':')
                tickets.append((name, ticket_number))
                total_characters += len(ticket_number)

            if not tickets:
                return None

            # Determine the stopping position on the roulette wheel
            stopping_position = total_characters % len(tickets)

            # Return the winner's name
            return tickets[stopping_position][0]
    except FileNotFoundError:
        return 'File not found'
    except Exception as e:
        return str(e)