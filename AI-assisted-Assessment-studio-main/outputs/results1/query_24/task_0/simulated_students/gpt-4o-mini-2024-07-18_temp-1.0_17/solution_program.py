def board_game_summary(results):
    import re
    score_dict = {}
    pattern = r'([A-Z])(\d+)'
    matches = re.findall(pattern, results)

    for player, score in matches:
        if player not in score_dict:
            score_dict[player] = 0
        score_dict[player] += int(score)

    if len(results) > 0 and len(matches) == 0:
        raise ValueError("Invalid format: No players found in results.")

    for i in range(len(results)):
        if (results[i].isalpha() and (i+1 >= len(results) or not results[i+1].isdigit())):
            raise ValueError(f"Invalid format: Player '{results[i]}' does not have an associated score.")
        if (results[i].isdigit() and (i == 0 or not results[i-1].isalpha())):
            raise ValueError(f"Invalid format: Score '{results[i]}' is not preceded by a player.")
 
    return score_dict