def board_game_summary(results):
    import re

    if not isinstance(results, str):
        raise ValueError('Results must be a string.')

    score_dict = {}
    pattern = re.compile(r'([A-Z])(\d+)')
    matches = pattern.findall(results)

    if not matches:
        raise ValueError('Invalid results format.')

    for player, score in matches:
        score = int(score)
        if score <= 0:
            raise ValueError(f'Score must be a positive integer for player {player}.')
        if player in score_dict:
            score_dict[player] += score
        else:
            score_dict[player] = score

    return score_dict