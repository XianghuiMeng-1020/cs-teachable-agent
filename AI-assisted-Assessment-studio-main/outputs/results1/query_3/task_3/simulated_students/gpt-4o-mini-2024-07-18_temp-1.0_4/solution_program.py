def dice_game_of_chance(bet_config):
    if not isinstance(bet_config, dict):
        return {'result': 'error', 'message': 'Invalid input. A dictionary is expected.'}
    
    bet_on = bet_config.get('bet_on')
    amount = bet_config.get('amount')
    
    # Validate inputs
    if not isinstance(bet_on, str) or not bet_on.isdigit() or (amount <= 0) or not isinstance(amount, int):
        return {'result': 'error', 'message': 'Invalid bet_on (must be a positive integer as string) or amount (must be a positive integer).'}
    
    # Convert the bet_on to integer
    bet_on = int(bet_on)
    
    # Deterministic pairs of dice rolls
    dice_rolls = [(3, 4), (5, 2), (1, 6), (6, 6), (2, 3), (4, 2), (1, 1), (2, 4)]
    sum_roll = sum(dice_rolls[0])  # always evaluating the first roll for simulation
    
    # Determine game result
    if sum_roll == bet_on:
        return {'result': 'win', 'final_amount': amount * 2}
    else:
        return {'result': 'lose', 'final_amount': 0}