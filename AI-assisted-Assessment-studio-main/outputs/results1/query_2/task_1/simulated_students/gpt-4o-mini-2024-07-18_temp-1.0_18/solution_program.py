def check_winner(participants_file, winner_file):
    try:
        with open(participants_file, 'r') as pf:
            participants = {line.strip() for line in pf}
        
        with open(winner_file, 'r') as wf:
            winner = wf.read().strip()
        
        return winner in participants
    except FileNotFoundError:
        raise FileNotFoundError('One of the files was not found.')