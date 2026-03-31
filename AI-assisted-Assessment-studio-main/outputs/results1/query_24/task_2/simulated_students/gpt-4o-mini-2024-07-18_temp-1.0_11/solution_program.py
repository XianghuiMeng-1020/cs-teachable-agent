def calculate_winner_score(filepath):
    scores = {}
    try:
        with open(filepath, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) != 2:
                    continue
                player_name, score_str = parts[0], parts[1]
                try:
                    score = int(score_str)
                except ValueError:
                    continue
                if player_name in scores:
                    scores[player_name] += score
                else:
                    scores[player_name] = score
    except FileNotFoundError:
        return None

    if not scores:
        return None

    winner = max(scores, key=scores.get)
    return (winner, scores[winner])