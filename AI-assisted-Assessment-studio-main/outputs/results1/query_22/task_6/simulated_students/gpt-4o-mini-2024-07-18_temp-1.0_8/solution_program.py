def log_scores(filename, players, scores):
    with open(filename, 'w') as f:
        for player, score in zip(players, scores):
            f.write(f'{player}: {score}\n')


def top_score(filename):
    scores_dict = {}
    highest_score = -1
    top_players = []

    with open(filename, 'r') as f:
        for line in f:
            name, score = line.strip().split(': ')
            score = int(score)
            scores_dict[name] = score

            if score > highest_score:
                highest_score = score
                top_players = [name]
            elif score == highest_score:
                top_players.append(name)

    return top_players