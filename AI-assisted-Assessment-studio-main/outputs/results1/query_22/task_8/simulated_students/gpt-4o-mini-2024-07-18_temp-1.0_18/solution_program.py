def record_scores(filename, players_scores):
    with open(filename, 'a') as f:
        for i, round_scores in enumerate(players_scores):
            f.write(f'Round {i + 1}: ' + ' '.join(map(str, round_scores)) + '\n')


def get_scores(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]