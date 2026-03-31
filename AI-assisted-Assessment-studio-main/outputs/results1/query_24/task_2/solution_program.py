def calculate_winner_score(filepath):
    scores = {}
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
                if name in scores:
                    scores[name] += score
                else:
                    scores[name] = score
        if not scores:
            return None
        return max(scores.items(), key=lambda item: item[1])
    except FileNotFoundError:
        return None