def process_scores(input_file, output_file):
    with open(input_file, 'r') as infile:
        scores = {}
        for line in infile:
            name, score = line.strip().split(',')
            score = float(score)
            if name in scores:
                scores[name].append(score)
            else:
                scores[name] = [score]

    averages = {name: sum(scores) / len(scores) for name, scores in scores.items()}
    sorted_averages = sorted(averages.items())

    with open(output_file, 'w') as outfile:
        for name, average in sorted_averages:
            outfile.write(f'{name},{average:.1f}\n')