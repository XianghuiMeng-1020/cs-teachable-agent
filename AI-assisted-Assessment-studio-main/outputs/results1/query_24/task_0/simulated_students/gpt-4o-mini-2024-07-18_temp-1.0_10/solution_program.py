def board_game_summary(results):
    import re

    if not isinstance(results, str) or len(results) == 0:
        raise ValueError("Invalid input: Results must be a non-empty string.")

    pattern = re.compile(r'([A-Z])(\d+)')
    score_dict = {}
    matches = pattern.findall(results)

    if not matches:
        raise ValueError("Invalid format: No valid player scores found in the results.")

    for player, score in matches:
        score = int(score)
        if score <= 0:
            raise ValueError(f"Invalid score for player {player}: {score} must be greater than 0.")
        if player in score_dict:
            score_dict[player] += score
        else:
            score_dict[player] = score

    return score_dict