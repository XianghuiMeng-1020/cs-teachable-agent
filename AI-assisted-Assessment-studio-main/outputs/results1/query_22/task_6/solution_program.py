def log_scores(filename, players, scores):
    with open(filename, 'w') as f:
        for player, score in zip(players, scores):
            f.write(f"{player}: {score}\n")


def top_score(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    scores = []
    for line in lines:
        name_score = line.split(': ')
        name = name_score[0]
        score = int(name_score[1].strip())
        scores.append((name, score))
    max_score = max(scores, key=lambda x: x[1])[1]
    top_players = [name for name, score in scores if score == max_score]
    return top_players
