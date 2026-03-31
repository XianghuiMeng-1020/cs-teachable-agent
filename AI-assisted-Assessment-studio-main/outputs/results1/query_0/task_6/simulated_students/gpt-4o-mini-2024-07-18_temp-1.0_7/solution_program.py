def play_game_of_chance(file_name, bet_amount, bet_guess):
    with open(file_name, 'r') as file:
        winning_numbers = file.readlines()

    winning_numbers = [int(num.strip()) for num in winning_numbers]
    matches = winning_numbers.count(bet_guess)

    if matches > 0:
        return bet_amount * (2 * matches - 1)
    else:
        return -bet_amount