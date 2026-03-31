def high_or_low_game(numbers: list, guesses: list) -> int:
    score = 0
    for i in range(len(guesses)):
        current_number = numbers[i]
        next_number = numbers[i + 1]
        if (guesses[i] == "high" and next_number > current_number) or 
           (guesses[i] == "low" and next_number < current_number):
            score += 1
    return score