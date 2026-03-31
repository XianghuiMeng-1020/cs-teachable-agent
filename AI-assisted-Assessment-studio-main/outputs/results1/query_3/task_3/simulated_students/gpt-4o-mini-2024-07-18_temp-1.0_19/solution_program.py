def dice_game_of_chance(bet_config):
    if not isinstance(bet_config, dict):
        return {'error': 'Invalid input, must be a dictionary.'}
    
    bet_on = bet_config.get('bet_on')
    amount = bet_config.get('amount')
    
    if not isinstance(bet_on, str) or not bet_on.isdigit() or int(bet_on) < 2 or int(bet_on) > 12:
        return {'error': 'Invalid bet number. Must be a string of a number between 2 and 12.'}
    
    if not isinstance(amount, int) or amount < 0:
        return {'error': 'Invalid bet amount. Must be a non-negative integer.'}
    
    # Define a deterministic sequence of dice rolls for testability
    rolls = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), 
             (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), 
             (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), 
             (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), 
             (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), 
             (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)]
    
    final_amount = amount
    won = False
    bet_on_value = int(bet_on)
    
    for roll in rolls:
        dice_sum = sum(roll)
        if dice_sum == bet_on_value:
            final_amount += amount  # win, get double the amount back
            won = True
            break
    
    if not won:
        final_amount -= amount  # lose, lose the bet amount
    
    result = 'win' if won else 'lose'
    return {'result': result, 'final_amount': final_amount}