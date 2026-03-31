def dice_game_of_chance(bet_config):
    if not isinstance(bet_config, dict):
        return {'result': 'error', 'message': 'Invalid input format.'}
    
    bet_on = bet_config.get('bet_on')
    amount = bet_config.get('amount')
    
    if not isinstance(bet_on, str) or not bet_on.isdigit() or int(bet_on) < 2 or int(bet_on) > 12:
        return {'result': 'error', 'message': 'Invalid bet on number.'}
    
    if not isinstance(amount, int) or amount <= 0:
        return {'result': 'error', 'message': 'Bet amount must be a positive integer.'}
    
    # Simulating deterministic dice rolls
    dice_rolls = [(3, 4), (5, 2), (1, 6), (2, 5), (4, 3), (6, 1), (6, 6), (5, 5)]
    
    for dice in dice_rolls:
        sum_dice = sum(dice)
        if sum_dice == int(bet_on):
            return {'result': 'win', 'final_amount': amount * 2}
    
    return {'result': 'lose', 'final_amount': 0}