def calculate_winner_board_game(file_path):
    with open(file_path, 'r') as file:
        players = file.readlines()
    
    max_average_score = -1
    winner = None
    
    for player in players:
        name, score, rounds = player.strip().split(':')
        score = int(score)
        rounds = int(rounds)
        average_score_per_round = score / rounds
        
        if (average_score_per_round > max_average_score or
            (average_score_per_round == max_average_score and rounds < players[winner]['rounds'])):
            max_average_score = average_score_per_round
            winner = {'name': name, 'rounds': rounds}
    
    return winner['name']