def record_scores(filename, players_scores):
    with open(filename, 'a') as file:
        for i, round_scores in enumerate(players_scores):
            line = f'Round {i + 1}: ' + ' '.join(map(str, round_scores)) + '\n'
            file.write(line)


def get_scores(filename):
    with open(filename, 'r') as file:
        return file.readlines()