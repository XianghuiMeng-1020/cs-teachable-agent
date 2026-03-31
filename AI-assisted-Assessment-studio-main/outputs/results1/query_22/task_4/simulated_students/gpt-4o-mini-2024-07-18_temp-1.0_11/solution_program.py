def tally_scores(file_path):
    scores = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                player, score = line.split(':')
                score = int(score)
                if player in scores:
                    scores[player] += score
                else:
                    scores[player] = score
    sorted_scores = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    return sorted_scores
