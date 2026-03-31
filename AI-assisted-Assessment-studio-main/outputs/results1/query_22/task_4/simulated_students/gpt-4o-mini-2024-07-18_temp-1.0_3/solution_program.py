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
    sorted_scores = sorted(scores.items(), key=lambda x: (-x[1], x[0]))
    return sorted_scores