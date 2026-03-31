def dice_game_of_chance(bet_config):
    if not isinstance(bet_config, dict):
        return {'result': 'error', 'message': 'Invalid input, please provide a dictionary.'}

    bet_on = bet_config.get('bet_on')
    amount = bet_config.get('amount')

    if not isinstance(bet_on, str) or not bet_on.isdigit() or int(bet_on) < 2 or int(bet_on) > 12:
        return {'result': 'error', 'message': 'Invalid bet value, must be a number between 2 and 12.'}
    if not isinstance(amount, int) or amount < 0:
        return {'result': 'error', 'message': 'Invalid bet amount, must be a non-negative integer.'}

    bet_on = int(bet_on)
    initial_amount = amount

    dice_rolls = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
                  (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
                  (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6),
                  (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6),
                  (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6),
                  (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)]

    for die1, die2 in dice_rolls:
        sum_dice = die1 + die2
        if sum_dice == bet_on:
            final_amount = initial_amount * 2
            return {'result': 'win', 'final_amount': final_amount}

    final_amount = 0
    return {'result': 'lose', 'final_amount': final_amount}