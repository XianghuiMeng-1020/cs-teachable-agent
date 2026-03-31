def calculate_total_score() -> int:
    total_score = 0
    with open('scores.txt', 'r') as file:
        for line in file:
            parts = line.split('  # ')
            scores = parts[1].strip().split(', ')
            total_score += sum(int(score) for score in scores)
    return total_score