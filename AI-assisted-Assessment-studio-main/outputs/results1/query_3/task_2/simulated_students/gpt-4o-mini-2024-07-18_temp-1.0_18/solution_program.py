def play_game_of_chance(strategy):
    outcome = 'win' if len(strategy) % 2 == 0 else 'lose'
    bet_win = strategy.get('win', 0)
    bet_lose = strategy.get('lose', 0)
    
    if outcome == 'win':
        balance = bet_win * 2 - bet_lose
    else:
        balance = -bet_lose
    
    return {'result': outcome, 'balance': balance}