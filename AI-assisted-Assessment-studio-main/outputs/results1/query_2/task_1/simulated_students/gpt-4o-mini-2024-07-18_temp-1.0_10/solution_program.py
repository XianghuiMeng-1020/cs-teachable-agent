def check_winner(participants_file, winner_file):
    try:
        with open(participants_file, 'r') as p_file:
            participants = {line.strip() for line in p_file}
        with open(winner_file, 'r') as w_file:
            winner = w_file.read().strip()
        return winner in participants
    except FileNotFoundError:
        raise FileNotFoundError('One of the provided file paths does not exist.')
    except Exception as e:
        raise e