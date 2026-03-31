def play_game_of_chance(strategy):
    num_keys = len(strategy.keys())
    outcome = 'win' if num_keys % 2 == 0 else 'lose'
    if outcome == 'win':
        balance = strategy['win'] * 2 - strategy.get('lose', 0)
    else:
        balance = -strategy['lose']
    return {'result': outcome, 'balance': balance}