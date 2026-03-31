def board_game_summary(results):
    if not isinstance(results, str):
        raise ValueError("The results must be a string.")
    import re
    player_scores = {}
    pattern = r'([A-Z])(\d+)'
    matches = re.findall(pattern, results)
    if not matches:
        raise ValueError("The results string is improperly formatted.")
    for player, score in matches:
        score = int(score)
        if player in player_scores:
            player_scores[player] += score
        else:
            player_scores[player] = score
    return player_scores