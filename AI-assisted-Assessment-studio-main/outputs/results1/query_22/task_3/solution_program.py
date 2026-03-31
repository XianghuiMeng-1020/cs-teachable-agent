def calculate_scores(input_file, output_file):
    scores = {}
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                player, game, score = line.split(',')
                if player not in scores:
                    scores[player] = 0
                scores[player] += int(score)
    results = []
    for player in sorted(scores.keys()):
        results.append(f"{player},{scores[player]}")
    with open(output_file, 'w') as file:
        for result in results:
            file.write(result + '\n')