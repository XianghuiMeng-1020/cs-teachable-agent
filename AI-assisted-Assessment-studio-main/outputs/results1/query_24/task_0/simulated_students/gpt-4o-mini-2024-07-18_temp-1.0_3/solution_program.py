def board_game_summary(results):
    if not results:
        raise ValueError("The results string is empty.")

    players_scores = {}
    i = 0
    length = len(results)

    while i < length:
        player = results[i]
        if player < 'A' or player > 'Z':
            raise ValueError(f"Invalid player identifier '{player}'. Must be an uppercase letter from A to Z.")
        i += 1

        score_start = i
        while i < length and results[i].isdigit():
            i += 1

        if i == score_start:
            raise ValueError(f"Missing score for player '{player}'.")

        score = int(results[score_start:i])
        if player in players_scores:
            players_scores[player] += score
        else:
            players_scores[player] = score

    return players_scores
