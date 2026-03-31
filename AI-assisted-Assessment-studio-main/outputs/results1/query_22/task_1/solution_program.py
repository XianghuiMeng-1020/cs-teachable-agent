def process_scores(input_file, output_file):
    players = {}
    with open(input_file, 'r') as f:
        for line in f:
            name, score = line.strip().split(',')
            score = float(score)
            if name in players:
                players[name].append(score)
            else:
                players[name] = [score]
    with open(output_file, 'w') as f:
        for name in sorted(players):
            average_score = sum(players[name]) / len(players[name])
            f.write(f'{name},{average_score}\n')