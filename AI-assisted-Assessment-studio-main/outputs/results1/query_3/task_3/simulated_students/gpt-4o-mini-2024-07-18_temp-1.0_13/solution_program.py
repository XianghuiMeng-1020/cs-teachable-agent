def dice_game_of_chance(bet_config):
    if not isinstance(bet_config, dict):
        return {'result': 'error', 'message': 'Invalid input, expected a dictionary.'}
    
    bet_on = bet_config.get('bet_on')
    amount = bet_config.get('amount')
    
    if not isinstance(bet_on, str) or not bet_on.isdigit():
        return {'result': 'error', 'message': 'Invalid bet_on value. It must be a string representing a number.'}
    if not isinstance(amount, int) or amount < 0:
        return {'result': 'error', 'message': 'Invalid amount. It must be a non-negative integer.'}
    
    bet_on = int(bet_on)
    
    dice_pairs = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), 
                  (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), 
                  (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), 
                  (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), 
                  (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), 
                  (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)]
    
    for dice1, dice2 in dice_pairs:
        roll_sum = dice1 + dice2
        if roll_sum == bet_on:
            return {'result': 'win', 'final_amount': amount * 2}
    
    return {'result': 'lose', 'final_amount': 0}