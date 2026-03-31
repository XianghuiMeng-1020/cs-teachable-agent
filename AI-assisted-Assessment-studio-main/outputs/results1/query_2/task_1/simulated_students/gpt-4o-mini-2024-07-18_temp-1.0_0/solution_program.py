def check_winner(participants_file, winner_file):
    try:
        with open(participants_file, 'r') as file:
            participants = {line.strip() for line in file}
        
        with open(winner_file, 'r') as file:
            winner = file.read().strip()
        
        return winner in participants
    except FileNotFoundError:
        raise FileNotFoundError('One of the files could not be found.')
    except Exception as e:
        raise Exception(f'An error occurred: {e}')