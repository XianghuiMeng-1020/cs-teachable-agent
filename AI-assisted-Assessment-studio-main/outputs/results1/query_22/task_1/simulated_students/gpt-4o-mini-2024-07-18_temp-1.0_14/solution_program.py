def process_scores(input_file, output_file):
    from collections import defaultdict
    import statistics

    scores = defaultdict(list)
    with open(input_file, 'r') as infile:
        for line in infile:
            name, score = line.strip().split(',')
            scores[name].append(float(score))

    averages = {name: statistics.mean(score_list) for name, score_list in scores.items()}
    sorted_averages = sorted(averages.items())

    with open(output_file, 'w') as outfile:
        for name, avg in sorted_averages:
            outfile.write(f'{name},{avg:.1f}\n')