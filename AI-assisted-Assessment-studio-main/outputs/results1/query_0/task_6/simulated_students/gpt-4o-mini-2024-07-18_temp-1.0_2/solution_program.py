def play_game_of_chance(file_name, bet_amount, bet_guess):
    if bet_guess < 1 or bet_guess > 10:
        return -bet_amount

    with open(file_name, 'r') as file:
        winning_numbers = [int(line.strip()) for line in file]

    match_count = winning_numbers.count(bet_guess)
    if match_count > 0:
        return (match_count * 2 * bet_amount) - bet_amount
    else:
        return -bet_amount