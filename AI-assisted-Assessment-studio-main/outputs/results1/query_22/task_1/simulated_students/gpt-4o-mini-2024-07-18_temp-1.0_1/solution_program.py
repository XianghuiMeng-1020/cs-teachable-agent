def process_scores(input_file, output_file):
    scores = {}
    with open(input_file, 'r') as infile:
        for line in infile:
            name, score = line.strip().split(',')
            score = float(score)
            if name not in scores:
                scores[name] = []
            scores[name].append(score)
    averages = {name: sum(score_list) / len(score_list) for name, score_list in scores.items()}
    sorted_averages = sorted(averages.items())
    with open(output_file, 'w') as outfile:
        for name, avg in sorted_averages:
            outfile.write(f'{name},{avg:.1f}\n')