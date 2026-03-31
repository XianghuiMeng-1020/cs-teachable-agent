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

    average_scores = {name: sum(score_list) / len(score_list) for name, score_list in scores.items()}

    with open(output_file, 'w') as outfile:
        for name in sorted(average_scores.keys()):
            outfile.write(f'{name},{average_scores[name]:.1f}\n')