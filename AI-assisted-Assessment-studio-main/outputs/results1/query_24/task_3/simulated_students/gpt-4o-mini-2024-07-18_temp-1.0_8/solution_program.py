def calculate_board_game_score(game_results):
    scoreboard = {}

    for result in game_results:
        try:
            winner, scores = result.split(':')
            score1, score2 = map(int, scores.split(','))
            if winner not in scoreboard:
                scoreboard[winner] = 0
            scoreboard[winner] += (score1 - score2)
        except (ValueError, IndexError):
            continue

    return scoreboard