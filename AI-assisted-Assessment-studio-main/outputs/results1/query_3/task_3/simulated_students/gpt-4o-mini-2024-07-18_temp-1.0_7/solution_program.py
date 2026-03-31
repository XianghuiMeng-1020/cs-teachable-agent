def dice_game_of_chance(bet_config):
    valid_bets = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
    dice_rolls = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), 
                  (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), 
                  (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), 
                  (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), 
                  (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), 
                  (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)]

    bet_on = bet_config.get('bet_on')
    amount = bet_config.get('amount')

    if not isinstance(bet_on, str) or bet_on not in valid_bets:
        return {'result': 'error', 'final_amount': 'Invalid bet number.'}
    if not isinstance(amount, int) or amount < 0:
        return {'result': 'error', 'final_amount': 'Invalid bet amount.'}

    initial_amount = amount
    roll_sum = 0

    for roll in dice_rolls:
        roll_sum = sum(roll)
        break  # Only take the first roll for this deterministic simulation

    if str(roll_sum) == bet_on:
        return {'result': 'win', 'final_amount': initial_amount * 2}
    else:
        return {'result': 'lose', 'final_amount': 0}