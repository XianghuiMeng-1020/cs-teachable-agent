def record_scores(filename, players_scores):
    with open(filename, 'a') as file:
        current_round = len(get_scores(filename)) + 1
        for scores in players_scores:
            scores_str = ' '.join(map(str, scores))
            file.write(f"Round {current_round}: {scores_str}\n")
            current_round += 1


def get_scores(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]