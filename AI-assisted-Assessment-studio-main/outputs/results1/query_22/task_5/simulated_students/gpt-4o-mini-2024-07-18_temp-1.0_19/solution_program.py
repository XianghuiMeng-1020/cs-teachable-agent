def calculate_winner_board_game(file_path):
    with open(file_path, 'r') as file:
        players = []  
        for line in file:
            player_name, score, rounds = line.strip().split(':')
            score = int(score)
            rounds = int(rounds)
            average_score = score / rounds
            players.append((player_name, average_score, rounds))

        winner = None
        highest_average = -1
        fewest_rounds = float('inf')

        for player in players:
            name, avg_score, rounds = player
            if (avg_score > highest_average) or (avg_score == highest_average and rounds < fewest_rounds):
                winner = name
                highest_average = avg_score
                fewest_rounds = rounds

        return winner