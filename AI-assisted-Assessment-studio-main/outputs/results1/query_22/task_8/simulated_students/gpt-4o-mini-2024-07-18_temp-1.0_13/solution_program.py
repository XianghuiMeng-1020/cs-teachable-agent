def record_scores(filename, players_scores):
    with open(filename, 'a') as file:
        for i, scores in enumerate(players_scores):
            file.write(f'Round {i + 1}: ' + ' '.join(map(str, scores)) + '\n')


def get_scores(filename):
    with open(filename, 'r') as file:
        return file.readlines()