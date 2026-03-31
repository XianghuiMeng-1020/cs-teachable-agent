def tally_scores(file_path):
    scores = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:  # ensure line is not empty
                player_name, score_str = line.split(":")
                score = int(score_str)
                if player_name in scores:
                    scores[player_name] += score
                else:
                    scores[player_name] = score
    # Convert the dictionary to a list of tuples and sort it
    sorted_scores = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    return sorted_scores
