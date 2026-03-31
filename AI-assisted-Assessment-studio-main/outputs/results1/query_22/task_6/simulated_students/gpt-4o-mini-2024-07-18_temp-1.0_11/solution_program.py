def log_scores(filename, players, scores):
    with open(filename, 'w') as file:
        for player, score in zip(players, scores):
            file.write(f'{player}: {score}\n')


def top_score(filename):
    with open(filename, 'r') as file:
        scores_dict = {}
        for line in file:
            name, score = line.strip().split(': ')
            scores_dict[name] = int(score)

        max_score = max(scores_dict.values())
        top_players = [name for name, score in scores_dict.items() if score == max_score]
        return top_players