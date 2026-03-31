def board_game_summary(results):
    import re
    score_dict = {}
    pattern = r'([A-Z])([1-9][0-9]*)'
    matches = re.findall(pattern, results)

    for player, score in matches:
        if player in score_dict:
            score_dict[player] += int(score)
        else:
            score_dict[player] = int(score)

    # Validate if all entries are properly formatted by checking if there are any unmatched parts
    if len(''.join([player + score for player, score in matches])) != len(results):
        raise ValueError('Invalid format in the results string.')

    return score_dict