def dice_game_of_chance(bet_config):
    if not isinstance(bet_config, dict):
        return {'result': 'error', 'final_amount': 0, 'message': 'Invalid input, provide a dictionary.'}

    bet_on = bet_config.get('bet_on')
    amount = bet_config.get('amount')

    if not isinstance(bet_on, str) or not bet_on.isdigit() or int(bet_on) < 2 or int(bet_on) > 12:
        return {'result': 'error', 'final_amount': 0, 'message': 'Invalid bet_on value.'}
    if not isinstance(amount, int) or amount < 0:
        return {'result': 'error', 'final_amount': 0, 'message': 'Invalid amount.'}

    bet_on = int(bet_on)
    initial_amount = amount

    deterministic_rolls = [(3, 4), (5, 2), (1, 6), (2, 2), (6, 1), (2, 4), (1, 1), (5, 5), (4, 6), (3, 3)]
    total_dice_rolls = len(deterministic_rolls)

    for i in range(total_dice_rolls):
        die1, die2 = deterministic_rolls[i]
        dice_sum = die1 + die2
        if dice_sum == bet_on:
            return {'result': 'win', 'final_amount': initial_amount * 2}

    return {'result': 'lose', 'final_amount': 0}