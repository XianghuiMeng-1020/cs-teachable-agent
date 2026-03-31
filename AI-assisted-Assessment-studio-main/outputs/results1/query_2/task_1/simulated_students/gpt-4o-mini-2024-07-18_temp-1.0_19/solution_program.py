def check_winner(participants_file, winner_file):
    try:
        with open(participants_file, 'r') as pf:
            participants = pf.read().strip().split('\n')

        with open(winner_file, 'r') as wf:
            winner = wf.read().strip()

        return winner in participants
    except FileNotFoundError:
        raise ValueError('One of the specified files does not exist.')
    except Exception as e:
        raise ValueError(f'An error occurred: {e}')