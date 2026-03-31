def dice_game_of_chance(bet_config):
    if not isinstance(bet_config, dict):
        return {'result': 'error', 'message': 'Invalid configuration'}

    bet_on = bet_config.get('bet_on')
    amount = bet_config.get('amount')

    if not isinstance(bet_on, str) or not bet_on.isdigit() or not isinstance(amount, int) or amount < 0:
        return {'result': 'error', 'message': 'Invalid bet configuration'}

    bet_on = int(bet_on)
    initial_amount = amount
    dice_rolls = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
                  (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
                  (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6),
                  (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6),
                  (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6),
                  (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)]

    for roll in dice_rolls:
        die1, die2 = roll
        total_roll = die1 + die2

        if total_roll == bet_on:
            return {'result': 'win', 'final_amount': initial_amount * 2}

    return {'result': 'lose', 'final_amount': 0}