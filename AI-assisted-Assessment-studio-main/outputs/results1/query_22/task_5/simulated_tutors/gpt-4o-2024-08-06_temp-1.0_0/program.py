def calculate_winner_board_game(file_path):
    with open(file_path, 'r') as file:
        players = []
        for line in file:
            # Parse each line
            player_name, score, rounds = line.strip().split(':')
            score = int(score)
            rounds = int(rounds)
            
            # Calculate average score per round
            average_score_per_round = score / rounds
            players.append((player_name, average_score_per_round, rounds))

    # Sort players first by highest average score, then by fewest rounds
    players.sort(key=lambda x: (-x[1], x[2]))

    # Return the player with the highest score
    return players[0][0]