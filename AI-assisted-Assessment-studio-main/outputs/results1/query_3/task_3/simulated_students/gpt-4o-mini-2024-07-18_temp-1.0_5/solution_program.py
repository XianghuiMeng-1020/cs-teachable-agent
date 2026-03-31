def dice_game_of_chance(bet_config):
    if not isinstance(bet_config, dict):
        return {'result': 'error', 'final_amount': 0, 'message': 'Invalid input format.'}

    bet_on = bet_config.get('bet_on')
    amount = bet_config.get('amount')

    if not isinstance(bet_on, str) or not bet_on.isdigit():
        return {'result': 'error', 'final_amount': 0, 'message': 'Invalid bet number.'}
    if not isinstance(amount, int) or amount <= 0:
        return {'result': 'error', 'final_amount': 0, 'message': 'Invalid bet amount.'}

    bet_on = int(bet_on)
    initial_amount = amount
    outcomes = [(2, 2), (3, 4), (5, 2), (1, 6), (4, 3), (6, 5), (1, 1), (3, 3), (2, 6), (4, 1), (5, 5), (6, 6)]
    bet_result = 'lose'
    final_amount = initial_amount

    for die1, die2 in outcomes:
        roll_sum = die1 + die2
        if roll_sum == bet_on:
            bet_result = 'win'
            final_amount += initial_amount
            break
        else:
            final_amount -= initial_amount

    return {'result': bet_result, 'final_amount': final_amount}