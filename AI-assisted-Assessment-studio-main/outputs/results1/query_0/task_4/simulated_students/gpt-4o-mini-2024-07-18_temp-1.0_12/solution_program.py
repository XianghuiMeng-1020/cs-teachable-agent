def calculate_total_score(filename):
    total_score = 0
    with open(filename, 'r') as file:
        for line in file:
            guess, outcome = map(int, line.strip().split(','))
            difference = abs(guess - outcome)
            if difference == 0:
                total_score += 100
            elif difference == 1:
                total_score += 50
            elif difference == 2:
                total_score += 20
            else:
                total_score += 0
    return total_score