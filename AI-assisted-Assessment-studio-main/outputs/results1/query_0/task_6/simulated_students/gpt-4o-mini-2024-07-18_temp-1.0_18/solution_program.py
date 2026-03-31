def play_game_of_chance(file_name, bet_amount, bet_guess):
    with open(file_name, 'r') as file:
        winning_numbers = file.readlines()

    winning_count = 0
    for number in winning_numbers:
        if int(number.strip()) == bet_guess:
            winning_count += 1

    if winning_count > 0:
        return bet_amount * (winning_count * 2 - 1)
    else:
        return -bet_amount