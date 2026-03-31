def check_winner(participants_file, winner_file):
    try:
        with open(participants_file, 'r') as f:
            participants = {line.strip() for line in f}
        with open(winner_file, 'r') as f:
            winner = f.read().strip()
        return winner in participants
    except FileNotFoundError:
        raise FileNotFoundError('One of the files does not exist')
    except Exception as e:
        raise Exception(f'An error occurred: {e}')