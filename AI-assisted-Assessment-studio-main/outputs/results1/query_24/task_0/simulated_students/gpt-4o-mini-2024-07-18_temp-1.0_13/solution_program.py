def board_game_summary(results):
    import re
    player_scores = {}
    pattern = re.compile(r'([A-Z])(\d+)')
    matches = pattern.findall(results)

    if not matches:
        raise ValueError('Invalid input format.')

    for player, score in matches:
        score_value = int(score)
        if player in player_scores:
            player_scores[player] += score_value
        else:
            player_scores[player] = score_value

    return player_scores