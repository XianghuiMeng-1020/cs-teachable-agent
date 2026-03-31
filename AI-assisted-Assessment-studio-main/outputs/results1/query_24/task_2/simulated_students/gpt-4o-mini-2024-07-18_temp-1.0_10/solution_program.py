def calculate_winner_score(filepath):
    player_scores = {}
    try:
        with open(filepath, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) != 2:
                    continue
                name, score_str = parts
                try:
                    score = int(score_str)
                except ValueError:
                    continue
                if name in player_scores:
                    player_scores[name] += score
                else:
                    player_scores[name] = score
        if not player_scores:
            return None  
        winner = max(player_scores.items(), key=lambda x: x[1])
        return winner
    except FileNotFoundError:
        return None
    except Exception as e:
        return None