def board_game_summary(results):
    from collections import defaultdict
    import re

    score_dict = defaultdict(int)

    # Regex to match player and their scores
    matches = re.findall(r'([A-Z])(\d+)', results)

    if not matches:
        raise ValueError("Improperly formatted results string.")

    for match in matches:
        player, score_str = match
        try:
            score = int(score_str)
            if score <= 0:
                raise ValueError(f"Invalid score for player {player}.")
            score_dict[player] += score
        except ValueError:
            raise ValueError(f"Invalid score format for player {player}: {score_str}.")

    return dict(score_dict)