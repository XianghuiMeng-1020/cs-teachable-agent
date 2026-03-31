def play_game_of_chance(strategy):
    if len(strategy.keys()) % 2 == 0:
        result = 'win'
        balance = strategy['win'] * 2 - strategy['lose']
    else:
        result = 'lose'
        balance = -strategy['lose']
    return {'result': result, 'balance': balance}