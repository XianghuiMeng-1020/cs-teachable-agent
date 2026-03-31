def dice_game_of_chance(bet_config):
    # Validate input:
    if not isinstance(bet_config, dict):
        return {'result': 'error', 'message': 'Invalid input format, dictionary expected.'}
    if 'bet_on' not in bet_config or 'amount' not in bet_config:
        return {'result': 'error', 'message': 'Missing required keys in configuration.'}
    if not isinstance(bet_config['amount'], int) or bet_config['amount'] < 0:
        return {'result': 'error', 'message': 'Bet amount must be a non-negative integer.'}
    if not isinstance(bet_config['bet_on'], str) or not bet_config['bet_on'].isdigit():
        return {'result': 'error', 'message': 'Bet must be a numeric string.'}

    bet_on = int(bet_config['bet_on'])
    amount = bet_config['amount']

    # Deterministic dice rolls for simulation
    dice_rolls = [(2, 3), (1, 4), (3, 3), (5, 2), (6, 6), (4, 5), (2, 6), (3, 5), (1, 1), (1, 2)]

    total_money = amount
    for roll in dice_rolls:
        roll_sum = sum(roll)
        if roll_sum == bet_on:
            total_money += amount  # Player wins
            return {'result': 'win', 'final_amount': total_money}
        else:
            total_money -= amount  # Player loses
            return {'result': 'lose', 'final_amount': total_money}

    return {'result': 'error', 'message': 'No more rolls available.'}