def calculate_total_score():
    total_score = 0
    with open('scores.txt', 'r') as file:
        for line in file:
            scores = line.split(', ')
            for score in scores:
                total_score += int(score)
    return total_score
