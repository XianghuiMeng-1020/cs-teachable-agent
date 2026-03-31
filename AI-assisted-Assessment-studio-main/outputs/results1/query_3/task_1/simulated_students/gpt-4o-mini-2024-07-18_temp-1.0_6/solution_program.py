def lottery_game(entries, winning_number):
    results = {}
    for participant, guess in entries.items():
        if guess == winning_number:
            results[participant] = 'Jackpot'
        elif guess in (winning_number - 1, winning_number + 1):
            results[participant] = 'Half-Pot'
        elif guess in (winning_number - 2, winning_number + 2):
            results[participant] = 'Quarter-Pot'
        else:
            results[participant] = 'No Winnings'
    return results