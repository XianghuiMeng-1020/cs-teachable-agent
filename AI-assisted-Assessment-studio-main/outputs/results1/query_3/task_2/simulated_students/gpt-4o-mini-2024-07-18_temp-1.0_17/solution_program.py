def play_game_of_chance(strategy):
    outcome = 'win' if len(strategy) % 2 == 0 else 'lose'
    balance = strategy[outcome] * 2 if outcome == 'win' else -strategy[outcome]
    return {'result': outcome, 'balance': balance}