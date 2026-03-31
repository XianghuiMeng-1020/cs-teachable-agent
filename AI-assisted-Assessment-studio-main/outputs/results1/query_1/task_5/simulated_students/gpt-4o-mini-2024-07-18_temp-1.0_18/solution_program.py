def high_or_low_game(numbers: list, guesses: list) -> int:
    score = 0
    for i in range(len(guesses)):
        if guesses[i] == "high":
            if numbers[i + 1] > numbers[i]:
                score += 1
        elif guesses[i] == "low":
            if numbers[i + 1] < numbers[i]:
                score += 1
    return score