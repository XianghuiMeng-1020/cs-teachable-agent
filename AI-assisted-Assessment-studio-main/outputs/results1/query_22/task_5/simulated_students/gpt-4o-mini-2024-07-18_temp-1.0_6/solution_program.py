def calculate_winner_board_game(file_path):
    with open(file_path, 'r') as file:
        players = file.readlines()
        max_avg_score = -1
        winner = ""

        for player in players:
            name, score, rounds = player.strip().split(':')
            score = int(score)
            rounds = int(rounds)
            avg_score = score / rounds

            if (avg_score > max_avg_score) or (avg_score == max_avg_score and rounds < players[winner][1]):
                max_avg_score = avg_score
                winner = name

        return winner