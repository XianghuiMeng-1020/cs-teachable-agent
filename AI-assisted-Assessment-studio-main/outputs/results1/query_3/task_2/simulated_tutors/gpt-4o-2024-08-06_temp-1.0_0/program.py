def play_game_of_chance(strategy):
    bets = len(strategy.keys())
    outcome = 'win' if bets % 2 == 0 else 'lose'

    if outcome == 'win':
        balance = strategy['win'] * 2 - strategy['lose']
    else:
        balance = -strategy['lose']

    return {'result': outcome, 'balance': balance}