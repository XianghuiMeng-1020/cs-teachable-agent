def calculate_total_score() -> int:
    total_score = 0
    with open('scores.txt', 'r') as file:
        for line in file:
            scores = line.strip().split('  # ')[1]
            scores_list = map(int, scores.split(','))
            total_score += sum(scores_list)
    return total_score