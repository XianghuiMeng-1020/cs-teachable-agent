def calculate_scores(input_file, output_file):
    scores = {}
    with open(input_file, 'r') as infile:
        for line in infile:
            player_name, game_name, score = line.strip().split(',')
            score = int(score)
            if player_name in scores:
                scores[player_name] += score
            else:
                scores[player_name] = score
    with open(output_file, 'w') as outfile:
        for player in sorted(scores.keys()):
            outfile.write(f'{player},{scores[player]}\n')