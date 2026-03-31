def play_game_of_chance(strategy):
    outcome = 'win' if len(strategy) % 2 == 0 else 'lose'
    if outcome == 'win':
        balance = strategy['win'] * 2 - strategy['lose']
    else:
        balance = -strategy['lose']
    return {'result': outcome, 'balance': balance}