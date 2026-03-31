def calculate_winner_score(filepath):
    scores = {}
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
                if player_name in scores:
                    scores[player_name] += score
                else:
                    scores[player_name] = score

        if not scores:
            return None

        winner = max(scores.items(), key=lambda item: item[1])
        return winner
    except FileNotFoundError:
        return None
