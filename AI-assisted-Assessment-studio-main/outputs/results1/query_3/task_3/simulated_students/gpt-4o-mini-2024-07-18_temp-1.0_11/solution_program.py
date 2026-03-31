def dice_game_of_chance(bet_config):
    valid_numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    dice_rolls = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
                  (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
                  (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6),
                  (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6),
                  (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6),
                  (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)]

    bet_on = bet_config.get('bet_on')
    amount = bet_config.get('amount')

    if not isinstance(bet_on, str) or not bet_on.isdigit():
        return {'result': 'error', 'message': 'Invalid bet number.'}
    if not isinstance(amount, int) or amount < 0:
        return {'result': 'error', 'message': 'Amount must be a non-negative integer.'}

    bet_on = int(bet_on)
    if bet_on not in valid_numbers:
        return {'result': 'error', 'message': 'Bet on a number between 2 and 12.'}

    # Simulate rolling the dice
    for roll in dice_rolls:
        first_die, second_die = roll
        total = first_die + second_die
        if total == bet_on:
            final_amount = amount * 2
            return {'result': 'win', 'final_amount': final_amount}
    final_amount = 0
    return {'result': 'lose', 'final_amount': final_amount}