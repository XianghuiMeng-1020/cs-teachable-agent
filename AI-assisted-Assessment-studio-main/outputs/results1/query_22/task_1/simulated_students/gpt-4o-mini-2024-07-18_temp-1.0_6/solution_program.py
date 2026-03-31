def process_scores(input_file, output_file):
    scores = {}
    with open(input_file, 'r') as infile:
        for line in infile:
            name, score = line.strip().split(',')
            score = float(score)
            if name in scores:
                scores[name].append(score)
            else:
                scores[name] = [score]
    averages = {name: sum(scores) / len(scores) for name, scores in scores.items()}
    with open(output_file, 'w') as outfile:
        for name in sorted(averages.keys()):
            outfile.write(f'{name},{averages[name]:.1f}\n')