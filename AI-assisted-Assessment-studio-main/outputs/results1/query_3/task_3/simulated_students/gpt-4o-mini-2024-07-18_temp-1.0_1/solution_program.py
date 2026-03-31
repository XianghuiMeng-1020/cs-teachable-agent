def dice_game_of_chance(bet_config):
    if not isinstance(bet_config, dict):
        return {'result': 'error', 'message': 'Invalid input format.'}
    
    bet_on = bet_config.get('bet_on')
    amount = bet_config.get('amount')
    
    if not isinstance(bet_on, str) or not bet_on.isnumeric() or int(bet_on) < 2 or int(bet_on) > 12:
        return {'result': 'error', 'message': 'Invalid bet number.'}
    
    if not isinstance(amount, int) or amount < 0:
        return {'result': 'error', 'message': 'Invalid bet amount.'}
    
    dice_rolls = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
                  (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
                  (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6),
                  (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6),
                  (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6),
                  (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)]
    
    total_amount = amount
    bets_on_char = int(bet_on)
    
    for dice_1, dice_2 in dice_rolls:
        total = dice_1 + dice_2
        if total == bets_on_char:
            total_amount += amount  
            return {'result': 'win', 'final_amount': total_amount}
        else:
            total_amount -= amount
            return {'result': 'lose', 'final_amount': total_amount}
    
    return {'result': 'error', 'message': 'Unexpected error.'}