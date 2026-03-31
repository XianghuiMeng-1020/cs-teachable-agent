def calculate_total_score() -> int:
    total_score = 0
    with open('scores.txt', 'r') as file:
        for line in file:
            scores = line.split('#')[-1].strip()  # Extract scores part
            score_list = map(int, scores.split(','))  # Convert scores to integers
            total_score += sum(score_list)  # Add to total score
    return total_score