def high_or_low_game(numbers, guesses):
    score = 0
    for i in range(len(guesses)):
        current = numbers[i]
        next_number = numbers[i + 1]
        guess = guesses[i]
        if guess == "high" and next_number > current:
            score += 1
        elif guess == "low" and next_number < current:
            score += 1
    return score