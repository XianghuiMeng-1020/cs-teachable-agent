def board_game_summary(results):
    if not results:
        raise ValueError("Results string cannot be empty.")

    player_scores = {}
    i = 0
    length = len(results)

    while i < length:
        player = results[i]
        i += 1
        if not player.isalpha() or len(player) != 1 or not ('A' <= player <= 'Z'):
            raise ValueError(f"Invalid player identifier: '{player}'.")

        score_start = i
        while i < length and results[i].isdigit():
            i += 1
        score_str = results[score_start:i]

        if not score_str:
            raise ValueError(f"Missing score for player '{player}'.")

        try:
            score = int(score_str)
        except ValueError:
            raise ValueError(f"Invalid score '{score_str}' for player '{player}'.")

        if player in player_scores:
            player_scores[player] += score
        else:
            player_scores[player] = score

    return player_scores