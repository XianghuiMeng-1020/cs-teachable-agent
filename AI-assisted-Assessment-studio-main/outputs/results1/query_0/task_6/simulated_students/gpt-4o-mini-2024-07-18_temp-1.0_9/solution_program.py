def play_game_of_chance(file_name, bet_amount, bet_guess):
    if bet_guess < 1 or bet_guess > 10:
        return -bet_amount

    with open(file_name, 'r') as file:
        results = file.readlines()

    win_count = 0
    for line in results:
        winning_number = int(line.strip())
        if winning_number == bet_guess:
            win_count += 1

    if win_count > 0:
        return (win_count * bet_amount * 2) - bet_amount
    else:
        return -bet_amount