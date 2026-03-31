def play_game_of_chance(file_name, bet_amount, bet_guess):
    if bet_guess < 1 or bet_guess > 10:
        return -bet_amount
    with open(file_name, 'r') as file:
        results = file.readlines()
    matches = sum(1 for line in results if int(line.strip()) == bet_guess)
    if matches > 0:
        return (2 * bet_amount * matches) - bet_amount
    else:
        return -bet_amount