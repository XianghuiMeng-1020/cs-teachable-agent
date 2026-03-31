def play_game_of_chance(file_name, bet_amount, bet_guess):
    with open(file_name, 'r') as file:
        winning_numbers = [int(line.strip()) for line in file]

    matches = winning_numbers.count(bet_guess)
    if matches > 0:
        return (matches * 2 * bet_amount) - bet_amount
    else:
        return -bet_amount