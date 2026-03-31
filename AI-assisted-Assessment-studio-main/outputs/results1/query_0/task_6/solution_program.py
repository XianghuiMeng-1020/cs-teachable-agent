def play_game_of_chance(file_name, bet_amount, bet_guess):
    with open(file_name, 'r') as file:
        numbers = file.readlines()
    matches = 0
    for number in numbers:
        if int(number.strip()) == bet_guess:
            matches += 1
    if matches > 0:
        return (2 * matches * bet_amount) - bet_amount
    else:
        return -bet_amount
