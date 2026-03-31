def dice_game_of_chance(bet_config):
    if not isinstance(bet_config, dict):
        return {'result': 'error', 'message': 'Invalid input, expected a dictionary.'}
    
    bet_on = bet_config.get('bet_on')
    amount = bet_config.get('amount')
    
    if not isinstance(bet_on, str) or not bet_on.isdigit() or not isinstance(amount, int):
        return {'result': 'error', 'message': 'Invalid bet or amount.'}
    
    bet_on = int(bet_on)
    if amount < 0:
        return {'result': 'error', 'message': 'Bet amount cannot be negative.'}
    
    # List of deterministic dice rolls (pairs)
    dice_rolls = [(3, 4), (5, 2), (1, 6), (6, 3), (4, 4), (2, 5), (1, 1)]
    
    for die1, die2 in dice_rolls:
        sum_roll = die1 + die2
        if sum_roll == bet_on:
            final_amount = amount * 2
            return {'result': 'win', 'final_amount': final_amount}
    
    return {'result': 'lose', 'final_amount': 0}