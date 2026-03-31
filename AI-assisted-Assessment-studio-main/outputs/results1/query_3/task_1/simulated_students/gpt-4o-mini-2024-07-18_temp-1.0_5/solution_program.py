def lottery_game(entries, winning_number):
    results = {}
    for participant, guessed_number in entries.items():
        if guessed_number == winning_number:
            results[participant] = 'Jackpot'
        elif guessed_number in {winning_number - 1, winning_number + 1}:
            results[participant] = 'Half-Pot'
        elif guessed_number in {winning_number - 2, winning_number + 2}:
            results[participant] = 'Quarter-Pot'
        else:
            results[participant] = 'No Winnings'
    return results