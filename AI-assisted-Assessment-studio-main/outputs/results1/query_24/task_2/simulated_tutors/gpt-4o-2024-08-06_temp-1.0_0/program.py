def calculate_winner_score(filepath):
    scores = {}
    try:
        with open(filepath, 'r') as file:
            for line in file:
                try:
                    name, score_str = line.split()
                    score = int(score_str)
                    if name in scores:
                        scores[name] += score
                    else:
                        scores[name] = score
                except ValueError:
                    return None
        max_score_player = max(scores, key=scores.get)
        return (max_score_player, scores[max_score_player])
    except FileNotFoundError:
        return None