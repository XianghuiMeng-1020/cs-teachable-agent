def board_game_summary(results):
    score_map = {}
    i = 0
    while i < len(results):
        if i < len(results) - 1 and results[i].isupper() and results[i + 1].isdigit():
            player = results[i]
            j = i + 1
            score = 0
            while j < len(results) and results[j].isdigit():
                score = score * 10 + int(results[j])
                j += 1
            if player in score_map:
                score_map[player] += score
            else:
                score_map[player] = score
            i = j
        else:
            raise ValueError(f'Improperly formatted data at index {i}: expected uppercase letter followed by digits.')
    return score_map