def calculate_winner_score(filepath):
    player_scores = {}
    try:
        with open(filepath, 'r') as file:
            for line in file:
                parts = line.split()
                if len(parts) != 2:
                    continue
                player_name, score_str = parts
                try:
                    score = int(score_str)
                except ValueError:
                    continue
                if player_name in player_scores:
                    player_scores[player_name] += score
                else:
                    player_scores[player_name] = score
        if not player_scores:
            return None
        winner = max(player_scores, key=player_scores.get)
        return (winner, player_scores[winner])
    except FileNotFoundError:
        return None