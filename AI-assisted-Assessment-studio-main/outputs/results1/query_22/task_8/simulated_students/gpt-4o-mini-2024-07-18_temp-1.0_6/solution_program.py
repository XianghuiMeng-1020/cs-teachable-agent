def record_scores(filename, players_scores):
    with open(filename, 'a') as file:
        for i, scores in enumerate(players_scores):
            round_scores = ' '.join(map(str, scores))
            file.write(f'Round {i + 1}: {round_scores}\n')


def get_scores(filename):
    with open(filename, 'r') as file:
        return file.readlines()