def check_winner(participants_file, winner_file):
    try:
        with open(participants_file, 'r') as p_file:
            participants = set(p_file.read().strip().split('\n'))
        with open(winner_file, 'r') as w_file:
            winner = w_file.read().strip()

        return winner in participants
    except FileNotFoundError:
        raise FileNotFoundError('One of the files could not be found.')
    except Exception as e:
        raise e