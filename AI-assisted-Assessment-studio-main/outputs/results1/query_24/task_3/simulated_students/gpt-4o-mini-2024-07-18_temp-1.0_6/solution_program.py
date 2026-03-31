def calculate_board_game_score(game_results):
    scores = {}
    for result in game_results:
        parts = result.split(':')
        if len(parts) != 2:
            continue
        winner = parts[0]
        score_parts = parts[1].split(',')
        if len(score_parts) != 2:
            continue
        try:
            score1 = int(score_parts[0])
            score2 = int(score_parts[1])
        except ValueError:
            continue
        if winner not in scores:
            scores[winner] = 0
        scores[winner] += (score1 - score2)
    return scores