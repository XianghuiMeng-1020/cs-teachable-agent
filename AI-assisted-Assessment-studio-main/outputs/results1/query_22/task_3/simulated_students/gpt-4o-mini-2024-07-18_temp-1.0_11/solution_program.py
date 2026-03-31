def calculate_scores(input_file, output_file):
    player_scores = {}
    
    with open(input_file, 'r') as infile:
        for line in infile:
            player_name, game_name, score = line.strip().split(',')
            score = int(score)
            if player_name in player_scores:
                player_scores[player_name] += score
            else:
                player_scores[player_name] = score
    
    sorted_players = sorted(player_scores.items())
    
    with open(output_file, 'w') as outfile:
        for player_name, total_score in sorted_players:
            outfile.write(f'{player_name},{total_score}\n')