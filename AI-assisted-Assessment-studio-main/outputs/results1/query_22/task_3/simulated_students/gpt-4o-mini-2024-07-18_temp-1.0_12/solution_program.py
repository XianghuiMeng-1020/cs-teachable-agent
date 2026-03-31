def calculate_scores(input_file, output_file):
    scores = {}
    with open(input_file, 'r') as infile:
        for line in infile:
            player_name, game_name, score = line.strip().split(',')
            score = int(score)
            if player_name not in scores:
                scores[player_name] = 0
            scores[player_name] += score

    sorted_scores = sorted(scores.items())
    with open(output_file, 'w') as outfile:
        for player_name, total_score in sorted_scores:
            outfile.write(f'{player_name},{total_score}\n')