def calculate_winner_score(filepath):
    scores = {}
    try:
        with open(filepath, 'r') as file:
            for line in file:
                # Split the line by whitespace
                parts = line.split()
                if len(parts) != 2:
                    continue
                player_name, score = parts[0], parts[1]
                try:
                    score = int(score)
                except ValueError:
                    continue
                # Add score to the player's total
                if player_name in scores:
                    scores[player_name] += score
                else:
                    scores[player_name] = score
    except FileNotFoundError:
        return None

    if not scores:
        return None

    # Determine the player with the highest score
    winner = max(scores.items(), key=lambda item: item[1])
    return winner
