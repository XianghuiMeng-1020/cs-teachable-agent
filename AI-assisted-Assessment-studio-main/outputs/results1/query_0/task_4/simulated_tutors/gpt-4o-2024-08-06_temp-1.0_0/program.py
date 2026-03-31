def calculate_total_score(filename):
    total_score = 0
    with open(filename, 'r') as file:
        for line in file:
            guess_str, actual_str = line.strip().split(',')
            guess = int(guess_str)
            actual = int(actual_str)
            difference = abs(guess - actual)
            if difference == 0:
                total_score += 100
            elif difference == 1:
                total_score += 50
            elif difference == 2:
                total_score += 20
    return total_score

# Test the function manually
# print(calculate_total_score('game_scores.txt'))