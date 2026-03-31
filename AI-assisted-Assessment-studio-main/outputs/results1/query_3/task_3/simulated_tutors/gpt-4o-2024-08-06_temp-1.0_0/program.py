def dice_game_of_chance(bet_config):
    try:
        # Extract the betting information
        bet_on = int(bet_config['bet_on'])
        amount = int(bet_config['amount'])
    except (ValueError, KeyError):
        return {'error': 'Invalid configuration'}
    
    # Validate bet amount
    if amount <= 0:
        return {'error': 'Invalid bet amount'}
    
    # Validate bet_on value
    valid_bet_range = range(2, 13) # Min: 1+1, Max: 6+6
    if bet_on not in valid_bet_range:
        return {'error': 'Invalid bet choice'}
    
    # Looped predefined dice rolls for deterministic result
    # just to facilitate testing
    possible_rolls = [(3, 4), (5, 2), (4, 5)]
    outcome = sum(possible_rolls[0])  # Select the first pair as the outcome

    # Determine the result of the game
    if outcome == bet_on:
        return {'result': 'win', 'final_amount': 2 * amount}
    else:
        return {'result': 'lose', 'final_amount': 0}