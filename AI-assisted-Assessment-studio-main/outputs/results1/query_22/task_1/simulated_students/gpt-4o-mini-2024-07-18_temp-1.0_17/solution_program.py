def process_scores(input_file, output_file):
    scores = {}
    counts = {}

    with open(input_file, 'r') as infile:
        for line in infile:
            name, score = line.strip().split(',')
            score = float(score)
            if name in scores:
                scores[name] += score
                counts[name] += 1
            else:
                scores[name] = score
                counts[name] = 1

    averages = {name: scores[name] / counts[name] for name in scores}
    sorted_averages = sorted(averages.items())

    with open(output_file, 'w') as outfile:
        for name, avg in sorted_averages:
            outfile.write(f'{name},{avg:.1f}\n')