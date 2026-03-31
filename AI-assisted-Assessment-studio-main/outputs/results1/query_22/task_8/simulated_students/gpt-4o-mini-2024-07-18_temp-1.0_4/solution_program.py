def record_scores(filename, players_scores):
    with open(filename, 'a') as f:
        for i, scores in enumerate(players_scores):
            line = f'Round {i + 1}: ' + ' '.join(map(str, scores))
            f.write(line + '\n')


def get_scores(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]