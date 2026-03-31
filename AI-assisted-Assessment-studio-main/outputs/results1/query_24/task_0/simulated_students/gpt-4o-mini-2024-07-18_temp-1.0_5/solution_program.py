def board_game_summary(results):
    import re
    score_dict = {}
    pattern = r'([A-Z])(\d+)'
    matches = re.findall(pattern, results)

    if not matches:
        raise ValueError('Invalid input format. No matches found. Ensure input follows the pattern.')

    for player, score in matches:
        if player not in score_dict:
            score_dict[player] = 0
        score_dict[player] += int(score)

    return score_dict