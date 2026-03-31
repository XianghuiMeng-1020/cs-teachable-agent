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

    average_scores = {name: sum(scores_list) / len(scores_list) for name, scores_list in scores.items()}
    sorted_average_scores = sorted(average_scores.items())

    with open(output_file, 'w') as outfile:
        for name, avg_score in sorted_average_scores:
            outfile.write(f'{name},{avg_score:.1f}\n')