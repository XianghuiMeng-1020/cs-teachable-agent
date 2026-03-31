def calculate_scores(input_file, output_file):
    player_scores = {}
    with open(input_file, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            player_name = parts[0]
            score = int(parts[2])
            if player_name in player_scores:
                player_scores[player_name] += score
            else:
                player_scores[player_name] = score
    with open(output_file, 'w') as f:
        for player in sorted(player_scores.keys()):
            f.write(f'{player},{player_scores[player]}
')