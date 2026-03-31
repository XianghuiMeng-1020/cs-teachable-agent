def calculate_total_score() -> int:
    total_score = 0
    with open('scores.txt', 'r') as file:
        for line in file:
            scores = line.split('#')[1].strip()
            score_list = map(int, scores.split(','))
            total_score += sum(score_list)
    return total_score