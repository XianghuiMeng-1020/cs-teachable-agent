def lottery_game(entries, winning_number):
    winnings = {}
    for participant, guess in entries.items():
        if guess == winning_number:
            winnings[participant] = 'Jackpot'
        elif abs(guess - winning_number) == 1:
            winnings[participant] = 'Half-Pot'
        elif abs(guess - winning_number) == 2:
            winnings[participant] = 'Quarter-Pot'
        else:
            winnings[participant] = 'No Winnings'
    return winnings