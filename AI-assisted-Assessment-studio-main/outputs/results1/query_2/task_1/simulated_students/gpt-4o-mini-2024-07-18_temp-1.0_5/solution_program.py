def check_winner(participants_file, winner_file):
    try:
        with open(participants_file, 'r') as f:
            participants = f.read().splitlines()
        with open(winner_file, 'r') as f:
            winner = f.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError("One of the specified files was not found.")
    return winner in participants