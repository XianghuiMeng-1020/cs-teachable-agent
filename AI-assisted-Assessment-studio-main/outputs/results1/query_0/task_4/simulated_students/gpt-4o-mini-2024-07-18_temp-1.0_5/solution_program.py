def calculate_total_score(filename):
    total_score = 0
    with open(filename, 'r') as file:
        for line in file:
            guess, outcome = map(int, line.strip().split(','))
            diff = abs(guess - outcome)
            if diff == 0:
                total_score += 100
            elif diff == 1:
                total_score += 50
            elif diff == 2:
                total_score += 20
    return total_score