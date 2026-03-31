def play_game_of_chance(file_name, bet_amount, bet_guess):
    if bet_guess < 1 or bet_guess > 10:
        return -bet_amount

    winnings = 0
    with open(file_name, 'r') as file:
        for line in file:
            winning_number = int(line.strip())
            if winning_number == bet_guess:
                winnings += 2 * bet_amount

    if winnings > 0:
        return winnings - bet_amount
    else:
        return -bet_amount