def calculate_total_score() -> int:
    total_score = 0
    with open('scores.txt', 'r') as file:
        for line in file:
            scores = line.strip().split('  # ')[1].split(', ')
            total_score += sum(int(score) for score in scores)
    return total_score