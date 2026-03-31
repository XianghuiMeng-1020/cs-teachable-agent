def calculate_total_score() -> int:
    total_score = 0
    with open('scores.txt', 'r') as file:
        for line in file:
            scores = line.split('#')[-1].strip().split(', ')
            total_score += sum(map(int, scores))
    return total_score