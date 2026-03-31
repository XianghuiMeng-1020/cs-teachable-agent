def play_dice_games(games):
    scores = {}
    for player, rolls in games.items():
        if len(rolls) == 3:
            scores[player] = sum(rolls)
        else:
            scores[player] = -1
    return scores