def record_scores(filename, players_scores):
    with open(filename, 'a') as file:
        for round_number, scores in enumerate(players_scores, start=1):
            score_line = f'Round {round_number}: {' '.join(map(str, scores))}'
            file.write(score_line + '\n')


def get_scores(filename):
    with open(filename, 'r') as file:
        return file.readlines()