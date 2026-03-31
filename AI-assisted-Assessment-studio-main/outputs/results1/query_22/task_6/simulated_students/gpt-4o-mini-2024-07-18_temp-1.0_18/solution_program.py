def log_scores(filename, players, scores):
    with open(filename, 'w') as file:
        for player, score in zip(players, scores):
            file.write(f'{player}: {score}\n')


def top_score(filename):
    max_score = -1
    top_players = []
    with open(filename, 'r') as file:
        for line in file:
            name, score = line.strip().split(': ')
            score = int(score)
            if score > max_score:
                max_score = score
                top_players = [name]
            elif score == max_score:
                top_players.append(name)
    return top_players