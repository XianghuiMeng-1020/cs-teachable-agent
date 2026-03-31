def calculate_winner_score(filepath):
    scores = {}
    try:
        with open(filepath, 'r') as file:
            for line in file:
                parts = line.split()
                if len(parts) != 2:
                    continue
                player, score_str = parts[0], parts[1]
                try:
                    score = int(score_str)
                    if player in scores:
                        scores[player] += score
                    else:
                        scores[player] = score
                except ValueError:
                    continue
    except FileNotFoundError:
        return None

    if not scores:
        return None
    winner = max(scores.items(), key=lambda item: item[1])
    return winner