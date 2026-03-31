def calculate_scores(input_file, output_file):
    scores = {}
    
    with open(input_file, 'r') as file:
        for line in file:
            player_name, game_name, score = line.strip().split(',')
            score = int(score)
            if player_name in scores:
                scores[player_name] += score
            else:
                scores[player_name] = score
    
    sorted_scores = sorted(scores.items())
    
    with open(output_file, 'w') as file:
        for player_name, total_score in sorted_scores:
            file.write(f'{player_name},{total_score}\n')