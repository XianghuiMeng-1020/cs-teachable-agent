def lottery_game(entries, winning_number):
    winnings = {}
    for participant, guessed_number in entries.items():
        if guessed_number == winning_number:
            winnings[participant] = 'Jackpot'
        elif guessed_number in {winning_number - 1, winning_number + 1 }:
            winnings[participant] = 'Half-Pot'
        elif guessed_number in {winning_number - 2, winning_number + 2 }:
            winnings[participant] = 'Quarter-Pot'
        else:
            winnings[participant] = 'No Winnings'
    return winnings