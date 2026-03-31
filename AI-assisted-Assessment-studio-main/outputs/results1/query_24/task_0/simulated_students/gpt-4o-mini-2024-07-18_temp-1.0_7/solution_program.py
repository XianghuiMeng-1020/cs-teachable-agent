def board_game_summary(results):
    import re
    pattern = r'([A-Z])(\d+)'
    matches = re.findall(pattern, results)
    score_dict = {}

    for player, score in matches:
        if player not in score_dict:
            score_dict[player] = 0
        score_dict[player] += int(score)

    if not matches:
        raise ValueError('Invalid input format: no valid player scores found.')

    return score_dict