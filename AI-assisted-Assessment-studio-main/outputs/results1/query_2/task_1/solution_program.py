def check_winner(participants_file, winner_file):
    with open(participants_file, 'r') as f:
        participants = f.read().splitlines()
    
    with open(winner_file, 'r') as f:
        winner = f.read().strip()

    return winner in participants
