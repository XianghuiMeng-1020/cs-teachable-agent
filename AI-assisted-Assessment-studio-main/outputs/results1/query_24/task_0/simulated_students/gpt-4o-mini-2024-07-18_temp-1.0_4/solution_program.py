def board_game_summary(results):
    import re
    score_dict = {}
    pattern = re.compile(r'([A-Z])(\d+)')
    matches = pattern.findall(results)

    if not matches:
        raise ValueError('Invalid format of results string.')

    for player, score in matches:
        if player not in score_dict:
            score_dict[player] = 0
        try:
            score_dict[player] += int(score)
        except ValueError:
            raise ValueError(f'Invalid score for player {player}: {score}')

    return score_dict