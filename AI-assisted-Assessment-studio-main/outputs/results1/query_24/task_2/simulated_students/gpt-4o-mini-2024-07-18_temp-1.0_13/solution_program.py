def calculate_winner_score(filepath):
    scores = {}
    try:
        with open(filepath, 'r') as file:
            for line in file:
                parts = line.split()
                if len(parts) != 2:
                    continue  # Skip any invalid line
                player_name, score_str = parts
                try:
                    score = int(score_str)
                    if player_name in scores:
                        scores[player_name] += score
                    else:
                        scores[player_name] = score
                except ValueError:
                    continue  # Skip if score is not an integer
    except FileNotFoundError:
        return None  # Handle the case where the file does not exist

    if not scores:
        return None  # Return None if there were no valid scores

    winner = max(scores.items(), key=lambda item: item[1])
    return winner