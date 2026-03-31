def dice_game_of_chance(bet_config):
    if not isinstance(bet_config, dict):
        return {'result': 'error', 'message': 'Invalid input: not a dictionary'}
    
    bet_on = bet_config.get('bet_on')
    amount = bet_config.get('amount')
    
    if not isinstance(bet_on, str) or not bet_on.isdigit() or int(bet_on) < 2 or int(bet_on) > 12:
        return {'result': 'error', 'message': 'Invalid bet_on value.'}
    
    if not isinstance(amount, int) or amount < 0:
        return {'result': 'error', 'message': 'Invalid amount: must be a non-negative integer.'}
    
    roll_sequence = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), 
                     (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), 
                     (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), 
                     (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), 
                     (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), 
                     (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)]
    
    total_amount = amount
    result = 'lose'
    
    for die1, die2 in roll_sequence:
        roll_sum = die1 + die2
        if roll_sum == int(bet_on):
            total_amount += amount  # Player wins double their bet amount
            result = 'win'
            break
    
    if result == 'lose':
        total_amount -= amount  # Player loses their bet amount
    
    return {'result': result, 'final_amount': total_amount}