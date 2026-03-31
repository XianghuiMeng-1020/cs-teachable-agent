def play_game_of_chance(file_name, bet_amount, bet_guess):
    if bet_guess < 1 or bet_guess > 10:
        return -bet_amount

    with open(file_name, 'r') as file:
        winning_numbers = file.readlines()

    winning_numbers = [int(number.strip()) for number in winning_numbers]
    matches = winning_numbers.count(bet_guess)

    if matches > 0:
        return (matches * 2 * bet_amount) - bet_amount
    else:
        return -bet_amount