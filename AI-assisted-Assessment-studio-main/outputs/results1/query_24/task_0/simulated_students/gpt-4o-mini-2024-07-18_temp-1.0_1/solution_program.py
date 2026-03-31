def board_game_summary(results):
    import re
    scores = {}
    pattern = re.compile(r'([A-Z])(\d+)')
    matches = pattern.findall(results)

    if not matches:
        raise ValueError("Results string is improperly formatted or empty.")

    for player, score in matches:
        try:
            score = int(score)
            if score <= 0:
                raise ValueError(f"Player '{player}' has a non-positive score: {score}.")
            if player in scores:
                scores[player] += score
            else:
                scores[player] = score
        except ValueError:
            raise ValueError(f"Invalid score for player '{player}': {score}.")

    return scores