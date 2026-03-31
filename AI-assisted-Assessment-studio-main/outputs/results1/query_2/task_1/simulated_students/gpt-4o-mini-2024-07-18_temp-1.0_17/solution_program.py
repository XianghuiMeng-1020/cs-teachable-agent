def check_winner(participants_file, winner_file):
    try:
        with open(participants_file, 'r') as pf:
            participants = pf.read().splitlines()
        with open(winner_file, 'r') as wf:
            winner = wf.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError("One of the files does not exist.")
    return winner in participants