def record_scores(filename, players_scores):
    with open(filename, 'a') as file:
        for i, round_scores in enumerate(players_scores):
            scores_line = f'Round {i + 1}: ' + ' '.join(map(str, round_scores))
            file.write(scores_line + '\n')


def get_scores(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]