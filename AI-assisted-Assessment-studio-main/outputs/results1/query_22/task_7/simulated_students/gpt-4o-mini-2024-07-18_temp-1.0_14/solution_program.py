def calculate_total_score() -> int:
    total_score = 0
    with open('scores.txt', 'r') as file:
        for line in file:
            _, scores = line.split('  # ')
            scores_list = list(map(int, scores.split(', ')))
            total_score += sum(scores_list)
    return total_score