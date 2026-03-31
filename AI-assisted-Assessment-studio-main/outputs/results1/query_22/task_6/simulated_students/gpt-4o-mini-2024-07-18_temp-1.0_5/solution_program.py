def log_scores(filename, players, scores):
    with open(filename, 'w') as file:
        for player, score in zip(players, scores):
            file.write(f'{player}: {score}\n')


def top_score(filename):
    with open(filename, 'r') as file:
        scores = {}
        for line in file:
            name, score = line.strip().split(': ')
            scores[name] = int(score)

    max_score = max(scores.values())
    return [name for name, score in scores.items() if score == max_score]