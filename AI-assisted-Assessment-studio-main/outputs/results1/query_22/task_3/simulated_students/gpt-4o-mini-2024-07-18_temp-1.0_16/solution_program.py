def calculate_scores(input_file, output_file):
    scores = {}
    with open(input_file, 'r') as f:
        for line in f:
            player_name, game_name, score = line.strip().split(',')
            score = int(score)
            if player_name in scores:
                scores[player_name] += score
            else:
                scores[player_name] = score
    sorted_scores = sorted(scores.items())
    with open(output_file, 'w') as f:
        for player, total_score in sorted_scores:
            f.write(f'{player},{total_score}\n')