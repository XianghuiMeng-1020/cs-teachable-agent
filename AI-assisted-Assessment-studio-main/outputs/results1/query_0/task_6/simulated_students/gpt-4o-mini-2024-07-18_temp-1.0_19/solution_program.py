def play_game_of_chance(file_name, bet_amount, bet_guess):
    with open(file_name, 'r') as file:
        winning_numbers = file.readlines()

    winning_numbers = [int(number.strip()) for number in winning_numbers]
    match_count = winning_numbers.count(bet_guess)

    if match_count > 0:
        return (match_count * 2 * bet_amount) - bet_amount
    else:
        return -bet_amount