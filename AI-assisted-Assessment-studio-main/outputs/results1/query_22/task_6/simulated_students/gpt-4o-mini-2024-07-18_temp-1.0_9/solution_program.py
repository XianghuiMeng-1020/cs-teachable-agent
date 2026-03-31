def log_scores(filename, players, scores):
    with open(filename, 'w') as f:
        for player, score in zip(players, scores):
            f.write(f'{player}: {score}\n')


def top_score(filename):
    scores = {}
    with open(filename, 'r') as f:
        for line in f:
            player, score = line.strip().split(': ')
            scores[player] = int(score)
    max_score = max(scores.values())
    return [player for player, score in scores.items() if score == max_score]