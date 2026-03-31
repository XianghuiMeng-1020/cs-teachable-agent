def play_game_of_chance(file_name, bet_amount, bet_guess):
    if bet_guess < 1 or bet_guess > 10:
        return -bet_amount

    with open(file_name, 'r') as file:
        results = file.readlines()

    matches = 0
    for line in results:
        if int(line.strip()) == bet_guess:
            matches += 1

    if matches > 0:
        return (matches * bet_amount * 2) - bet_amount
    else:
        return -bet_amount