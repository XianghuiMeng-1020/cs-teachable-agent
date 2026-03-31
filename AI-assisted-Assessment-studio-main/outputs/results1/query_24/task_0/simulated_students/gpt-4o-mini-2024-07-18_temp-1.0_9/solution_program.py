def board_game_summary(results):
    scores = {}
    i = 0
    while i < len(results):
        player = results[i]
        if not player.isalpha() or not player.isupper():
            raise ValueError(f"Invalid player character at index {i}: '{player}'")
        i += 1
        score_str = ''
        while i < len(results) and results[i].isdigit():
            score_str += results[i]
            i += 1
        if score_str == '':
            raise ValueError(f"No score found for player '{player}' at index {i-1}")
        score = int(score_str)
        if player in scores:
            scores[player] += score
        else:
            scores[player] = score
    return scores