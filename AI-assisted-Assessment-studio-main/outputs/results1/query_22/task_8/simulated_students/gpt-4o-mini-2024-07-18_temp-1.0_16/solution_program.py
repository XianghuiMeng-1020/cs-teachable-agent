def record_scores(filename, players_scores):
    with open(filename, 'a') as file:
        for round_number, scores in enumerate(players_scores, start=1):
            scores_str = ' '.join(map(str, scores))
            file.write(f'Round {round_number}: {scores_str}\n')


def get_scores(filename):
    with open(filename, 'r') as file:
        return file.readlines()