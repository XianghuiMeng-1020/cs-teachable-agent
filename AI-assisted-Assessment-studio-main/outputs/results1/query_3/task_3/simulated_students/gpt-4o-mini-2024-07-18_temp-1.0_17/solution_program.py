def dice_game_of_chance(bet_config):
    if not isinstance(bet_config, dict):
        return {'result': 'error', 'message': 'Invalid input format.'}
    
    bet_on = bet_config.get('bet_on')
    amount = bet_config.get('amount')
    
    try:
        bet_on = int(bet_on)
        if amount < 0:
            return {'result': 'error', 'message': 'Bet amount must be positive.'}
    except (ValueError, TypeError):
        return {'result': 'error', 'message': 'Invalid bet number.'}
    
    pairs_of_dice = [(1, 1), (2, 3), (3, 4), (4, 2), (5, 5), (6, 6)]
    for dice in pairs_of_dice:
        dice_sum = sum(dice)
        if dice_sum == bet_on:
            final_amount = amount * 2
            return {'result': 'win', 'final_amount': final_amount}
    
    final_amount = 0
    return {'result': 'lose', 'final_amount': final_amount}