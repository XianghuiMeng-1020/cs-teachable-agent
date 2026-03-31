def calculate_total_score() -> int:
    total_score = 0
    with open('scores.txt', 'r') as file:
        for line in file:
            parts = line.strip().split('  # ')
            scores = parts[1].split(', ')
            total_score += sum(int(score) for score in scores)
    return total_score