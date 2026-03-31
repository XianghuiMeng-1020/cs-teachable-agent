def dice_game_of_chance(bet_config):
    bet_on = bet_config.get('bet_on')
    amount = bet_config.get('amount')
    allowed_rolls = [(3, 4), (2, 5), (6, 3), (4, 3), (5, 4)]
    
    if not str(bet_on).isdigit() or int(bet_on) <= 0:
        return {'error': 'Invalid bet choice'}
    if amount <= 0:
        return {'error': 'Invalid bet amount'}
    
    for roll in allowed_rolls:
        sum_dice = roll[0] + roll[1]
        if sum_dice == int(bet_on):
            return {'result': 'win', 'final_amount': amount * 2}
        else:
            return {'result': 'lose', 'final_amount': 0}
    return {'result': 'lose', 'final_amount': 0}