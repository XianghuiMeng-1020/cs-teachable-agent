def play_dice_games(games):
    results = {}
    for player, rolls in games.items():
        if len(rolls) != 3:
            results[player] = -1
        else:
            results[player] = sum(rolls)
    return results