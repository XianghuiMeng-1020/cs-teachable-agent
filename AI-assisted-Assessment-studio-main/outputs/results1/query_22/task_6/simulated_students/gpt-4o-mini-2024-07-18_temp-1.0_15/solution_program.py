def log_scores(filename, players, scores):
    with open(filename, 'w') as f:
        for player, score in zip(players, scores):
            f.write(f'{player}: {score}\n')


def top_score(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        max_score = -1
        top_players = []
        for line in lines:
            name, score = line.strip().split(': ')
            score = int(score)
            if score > max_score:
                max_score = score
                top_players = [name]
            elif score == max_score:
                top_players.append(name)
        return top_players