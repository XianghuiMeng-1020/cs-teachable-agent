def calculate_winner_score(filepath):
    scores = {}
    try:
        with open(filepath, 'r') as file:
            for line in file:
                parts = line.split()
                if len(parts) != 2:
                    continue
                player_name = parts[0]
                try:
                    score = int(parts[1])
                except ValueError:
                    continue
                if player_name in scores:
                    scores[player_name] += score
                else:
                    scores[player_name] = score
    except FileNotFoundError:
        return (None, 0)

    if not scores:
        return (None, 0)

    winner = max(scores.items(), key=lambda item: item[1])
    return winner