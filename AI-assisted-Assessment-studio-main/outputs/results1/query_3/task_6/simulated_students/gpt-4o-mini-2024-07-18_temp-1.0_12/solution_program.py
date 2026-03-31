def play_dice_games(games):
    result = {}
    for player, rolls in games.items():
        if len(rolls) != 3:
            result[player] = -1
        else:
            result[player] = sum(rolls)
    return result