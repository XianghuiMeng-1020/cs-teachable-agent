def dice_game_of_chance(bet_config):
    valid_bets = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}
    results = [ (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
                (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
                (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6),
                (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6),
                (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6),
                (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6) ]

    if not isinstance(bet_config, dict):
        return {'result': 'error', 'final_amount': 'Invalid bet configuration'}
    if 'bet_on' not in bet_config or 'amount' not in bet_config:
        return {'result': 'error', 'final_amount': 'Incorrect keys in bet configuration'}

    bet_on = bet_config['bet_on']
    amount = bet_config['amount']

    if not isinstance(bet_on, str) or not bet_on.isdigit() or int(bet_on) not in valid_bets:
        return {'result': 'error', 'final_amount': 'Invalid bet on number'}
    if not isinstance(amount, int) or amount < 0:
        return {'result': 'error', 'final_amount': 'Invalid bet amount'}

    initial_amount = amount
    for die1, die2 in results:
        sum_dice = die1 + die2
        if sum_dice == int(bet_on):
            return {'result': 'win', 'final_amount': initial_amount * 2}

    return {'result': 'lose', 'final_amount': 0}