def board_game_summary(results):
    import re
    score_dict = {}
    pattern = re.compile(r'([A-Z])(\d+)')
    matches = pattern.findall(results)

    if not matches:
        raise ValueError('Invalid input format.')

    for player, score in matches:
        score_value = int(score)
        if player in score_dict:
            score_dict[player] += score_value
        else:
            score_dict[player] = score_value

    return score_dict