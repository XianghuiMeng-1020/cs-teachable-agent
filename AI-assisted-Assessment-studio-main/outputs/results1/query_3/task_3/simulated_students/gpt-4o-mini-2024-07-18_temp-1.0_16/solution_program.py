def dice_game_of_chance(bet_config):
    # Validate input
    try:
        bet_on = int(bet_config['bet_on'])
        amount = int(bet_config['amount'])
        if amount < 0:
            return {'result': 'error', 'message': 'Bet amount must be a positive integer.'}
    except (ValueError, KeyError):
        return {'result': 'error', 'message': 'Invalid input. Ensure bet_on is an integer and amount is a positive integer.'}

    # Pair of dice rolls
    dice_rolls = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)]
    initial_amount = amount

    for dice in dice_rolls:
        dice_sum = sum(dice)
        if dice_sum == bet_on:
            final_amount = initial_amount + amount
            return {'result': 'win', 'final_amount': final_amount}

    final_amount = initial_amount - amount
    return {'result': 'lose', 'final_amount': final_amount}