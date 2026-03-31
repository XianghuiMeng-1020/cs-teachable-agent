def play_game_of_chance(file_name, bet_amount, bet_guess):
    if bet_guess < 1 or bet_guess > 10:
        return -bet_amount
    wins = 0
    with open(file_name, 'r') as file:
        for line in file:
            winning_number = int(line.strip())
            if winning_number == bet_guess:
                wins += 1
    if wins > 0:
        return (wins * bet_amount) - bet_amount
    else:
        return -bet_amount