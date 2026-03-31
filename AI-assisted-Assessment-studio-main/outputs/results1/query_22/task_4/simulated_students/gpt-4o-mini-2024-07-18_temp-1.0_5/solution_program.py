def tally_scores(file_path):
    scores = {}
    with open(file_path, 'r') as file:
        for line in file:
            player_name, score = line.strip().split(':')
            score = int(score)
            if player_name in scores:
                scores[player_name] += score
            else:
                scores[player_name] = score
    total_scores = [(name, total) for name, total in scores.items()]
    return sorted(total_scores, key=lambda x: (-x[1], x[0]))