def tally_scores(file_path):
    scores = {}
    with open(file_path, 'r') as file:
        for line in file:
            player, score = line.strip().split(':')
            score = int(score)
            if player in scores:
                scores[player] += score
            else:
                scores[player] = score
    result = sorted(scores.items(), key=lambda x: (-x[1], x[0]))
    return result