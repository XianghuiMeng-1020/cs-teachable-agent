def calculate_board_game_score(game_results):
    scores = {}
    for result in game_results:
        try:
            winner, score_part = result.split(":")
            score1, score2 = map(int, score_part.split(","))
            if winner.isalpha() and len(winner) == 1:
                # Calculate the score difference
                score_diff = score1 - score2
                # Add the score difference to the respective winner
                if winner in scores:
                    scores[winner] += score_diff
                else:
                    scores[winner] = score_diff
        except (ValueError, IndexError):
            # Ignore entries that cause errors
            continue
    return scores
