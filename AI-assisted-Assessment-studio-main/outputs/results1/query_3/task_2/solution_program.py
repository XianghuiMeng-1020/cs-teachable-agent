def play_game_of_chance(strategy):
    outcome = len(strategy) % 2
    if outcome == 0:
        return {'result': 'win', 'balance': strategy['win']}
    else:
        return {'result': 'lose', 'balance': -strategy['lose']}