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
    
    total_scores = [(player, total) for player, total in scores.items()]
    total_scores.sort(key=lambda x: (-x[1], x[0]))
    return total_scores