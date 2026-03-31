def log_scores(filename, players, scores):
    with open(filename, 'w') as f:
        for player, score in zip(players, scores):
            f.write(f'{player}: {score}\n')


def top_score(filename):
    with open(filename, 'r') as f:
        scores = {}
        for line in f:
            name, score = line.strip().split(': ')
            scores[name] = int(score)

    max_score = max(scores.values())
    top_players = [name for name, score in scores.items() if score == max_score]
    return top_players