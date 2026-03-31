def process_scores(input_file, output_file):
    scores = {}
    with open(input_file, 'r') as f:
        for line in f:
            name, score = line.strip().split(',')
            score = float(score)
            if name in scores:
                scores[name].append(score)
            else:
                scores[name] = [score]
    averages = {name: sum(score_list) / len(score_list) for name, score_list in scores.items()}
    with open(output_file, 'w') as f:
        for name in sorted(averages.keys()):
            f.write(f'{name},{averages[name]:.1f}\n')