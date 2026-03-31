def high_or_low_game(numbers: list, guesses: list) -> int:
    score = 0
    for i in range(len(guesses)):
        current = numbers[i]
        next = numbers[i + 1]

        # Check the guess and increment the score accordingly
        if guesses[i] == "high" and next > current:
            score += 1
        elif guesses[i] == "low" and next < current:
            score += 1

    return score

# Example Usage:
example_numbers = [3, 8, 4]
example_guesses = ["high", "low"]
print(high_or_low_game(example_numbers, example_guesses))  # Output: 2