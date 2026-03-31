def dice_game_of_chance(bet_config):
    valid_bets = set(map(str, range(2, 13)))  # valid sums from two dice
    bet_on = bet_config.get('bet_on')
    amount = bet_config.get('amount')

    if bet_on not in valid_bets:
        return {'result': 'error', 'message': 'Invalid bet number. Must be between 2 and 12.'}
    if not isinstance(amount, int) or amount < 0:
        return {'result': 'error', 'message': 'Bet amount must be a non-negative integer.'}

    player_amount = amount
    dice_rolls = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), 
                  (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), 
                  (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), 
                  (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), 
                  (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), 
                  (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)]  # deterministic dice rolls

    for roll in dice_rolls:
        sum_of_dice = roll[0] + roll[1]
        if str(sum_of_dice) == bet_on:
            player_amount += amount  # win, keep original plus double the bet
            return {'result': 'win', 'final_amount': player_amount}

    player_amount -= amount  # lose, subtract bet amount
    return {'result': 'lose', 'final_amount': player_amount}