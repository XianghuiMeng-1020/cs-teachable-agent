def dice_game_of_chance(bet_config):
    if not isinstance(bet_config, dict):
        return {'result': 'error', 'message': 'Input must be a dictionary.'}
    
    bet_on = bet_config.get('bet_on')
    amount = bet_config.get('amount')
    
    if not isinstance(bet_on, str) or not bet_on.isdigit() or int(bet_on) < 2 or int(bet_on) > 12:
        return {'result': 'error', 'message': 'bet_on must be a valid string representing a number between 2 and 12.'}
    
    if not isinstance(amount, int) or amount < 0:
        return {'result': 'error', 'message': 'amount must be a non-negative integer.'}
    
    total_amount = amount
    
    # Deterministically simulate rolling the dice with fixed pairs
    fixed_pairs = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), 
                   (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), 
                   (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), 
                   (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), 
                   (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), 
                   (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)]
    
    for dice1, dice2 in fixed_pairs:
        dice_sum = dice1 + dice2
        if dice_sum == int(bet_on):
            total_amount += amount  # Player wins and gets double the bet
            return {'result': 'win', 'final_amount': total_amount}
    
    total_amount -= amount  # Player loses their bet
    return {'result': 'lose', 'final_amount': total_amount}