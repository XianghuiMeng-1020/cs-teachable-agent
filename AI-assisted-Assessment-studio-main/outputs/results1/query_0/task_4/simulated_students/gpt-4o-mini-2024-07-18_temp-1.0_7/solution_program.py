def calculate_total_score(filename):
    total_score = 0
    with open(filename, 'r') as file:
        for line in file:
            guess, actual = map(int, line.strip().split(','))
            score = 0
            if guess == actual:
                score = 100
            elif abs(guess - actual) == 1:
                score = 50
            elif abs(guess - actual) == 2:
                score = 20
            total_score += score
    return total_score