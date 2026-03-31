def calculate_total_score() -> int:
    total_score = 0
    with open('scores.txt', 'r') as file:
        for line in file:
            # Split the line into scores
            scores_part = line.split('  # ')[1]
            scores = map(int, scores_part.split(','))
            # Sum scores and add to total
            total_score += sum(scores)
    return total_score