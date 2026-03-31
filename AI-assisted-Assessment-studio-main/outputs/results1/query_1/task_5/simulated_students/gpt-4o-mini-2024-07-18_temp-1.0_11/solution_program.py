def high_or_low_game(numbers: list, guesses: list) -> int:
    score = 0
    
    for i in range(len(guesses)):
        current_number = numbers[i]
        next_number = numbers[i + 1]
        guess = guesses[i]
        
        if guess == "high" and next_number > current_number:
            score += 1
        elif guess == "low" and next_number < current_number:
            score += 1
    
    return score