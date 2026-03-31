def calculate_board_game_score(game_results):
    scores = {}
    for entry in game_results:
        try:
            winner, results = entry.split(':')
            score1, score2 = map(int, results.split(','))
            if winner not in scores:
                scores[winner] = 0
            scores[winner] += score1 - score2
        except (ValueError, IndexError):
            pass
    return scores