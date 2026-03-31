def play_game_of_chance(file_name, bet_amount, bet_guess):
    if bet_guess < 1 or bet_guess > 10:
        return -bet_amount  

    with open(file_name, 'r') as file:
        winning_numbers = file.readlines()

    count_matches = sum(1 for number in winning_numbers if int(number.strip()) == bet_guess)

    if count_matches > 0:
        return bet_amount * count_matches + (bet_amount - bet_amount)
    else:
        return -bet_amount