def play_game_of_chance(strategy):
    outcome_index = len(strategy) % 2
    if outcome_index == 0:
        result = 'win'
        balance = strategy['win'] * 2 - strategy['lose']
    else:
        result = 'lose'
        balance = -strategy['lose']
    return {'result': result, 'balance': balance}