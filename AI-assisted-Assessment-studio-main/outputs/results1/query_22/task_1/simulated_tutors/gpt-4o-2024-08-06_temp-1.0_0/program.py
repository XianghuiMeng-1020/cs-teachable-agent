def process_scores(input_file, output_file):
    # Dictionary to store total scores and count of scores for each player.
    scores = {}
    
    # Read input file
    with open(input_file, 'r') as f:
        for line in f:
            # Strip each line of whitespace and split at the comma
            name, score = line.strip().split(',')
            score = float(score)
            
            # If player is not in the dictionary, add them
            if name not in scores:
                scores[name] = {'total': 0, 'count': 0}
            
            # Update total score and count for player
            scores[name]['total'] += score
            scores[name]['count'] += 1

    # Calculate average scores and sort by player's name
    averages = []
    for name in sorted(scores.keys()):
        total = scores[name]['total']
        count = scores[name]['count']
        avg_score = total / count
        averages.append(f"{name},{avg_score}")
    
    # Write the averages to output file
    with open(output_file, 'w') as f:
        for line in averages:
            f.write(line + '\n')