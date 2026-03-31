def tally_scores(file_path):
    score_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            player_name, score = line.strip().split(':')
            score = int(score)
            if player_name in score_dict:
                score_dict[player_name] += score
            else:
                score_dict[player_name] = score
    sorted_scores = sorted(score_dict.items(), key=lambda x: (-x[1], x[0]))
    return sorted_scores