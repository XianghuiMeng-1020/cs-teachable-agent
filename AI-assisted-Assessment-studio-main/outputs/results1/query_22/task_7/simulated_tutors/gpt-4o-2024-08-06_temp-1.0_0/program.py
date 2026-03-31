def calculate_total_score() -> int:
    total_score = 0
    with open('scores.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            scores = line.split(',')
            scores_int = map(int, scores)
            total_score += sum(scores_int)
    return total_score