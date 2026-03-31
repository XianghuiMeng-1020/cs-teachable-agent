def calculate_total_score(filename):
    total_score = 0
    with open(filename, 'r') as file:
        for line in file:
            guess, actual = map(int, line.strip().split(','))
            if guess == actual:
                total_score += 100
            elif abs(guess - actual) == 1:
                total_score += 50
            elif abs(guess - actual) == 2:
                total_score += 20
            else:
                total_score += 0
    return total_score