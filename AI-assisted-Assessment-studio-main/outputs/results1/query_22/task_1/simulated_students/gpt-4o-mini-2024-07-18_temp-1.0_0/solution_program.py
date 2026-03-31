def process_scores(input_file, output_file):
    player_scores = {}
    player_counts = {}
    
    with open(input_file, 'r') as infile:
        for line in infile:
            name, score = line.strip().split(',')
            score = float(score)
            if name in player_scores:
                player_scores[name] += score
                player_counts[name] += 1
            else:
                player_scores[name] = score
                player_counts[name] = 1
    
    averages = {name: player_scores[name] / player_counts[name] for name in player_scores}
    sorted_averages = sorted(averages.items())
    
    with open(output_file, 'w') as outfile:
        for name, avg_score in sorted_averages:
            outfile.write(f'{name},{avg_score:.1f}\n')