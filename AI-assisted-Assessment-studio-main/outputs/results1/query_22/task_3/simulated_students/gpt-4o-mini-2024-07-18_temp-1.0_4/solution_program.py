def calculate_scores(input_file, output_file):
    scores = {}

    with open(input_file, 'r') as file:
        for line in file:
            player, game, score = line.strip().split(',')
            score = int(score)
            if player in scores:
                scores[player] += score
            else:
                scores[player] = score

    sorted_scores = sorted(scores.items())

    with open(output_file, 'w') as file:
        for player, total_score in sorted_scores:
            file.write(f'{player},{total_score}\n')