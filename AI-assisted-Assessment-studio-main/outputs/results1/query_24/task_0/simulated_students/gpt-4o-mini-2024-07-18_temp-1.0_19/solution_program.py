def board_game_summary(results):
    scores = {}
    i = 0
    n = len(results)

    while i < n:
        if i + 1 < n and results[i].isupper() and results[i + 1].isdigit():
            player = results[i]
            j = i + 1
            score_str = ''

            while j < n and results[j].isdigit():
                score_str += results[j]
                j += 1

            score = int(score_str)

            if player in scores:
                scores[player] += score
            else:
                scores[player] = score

            i = j
        else:
            raise ValueError(f'Invalid format at position {i}: {results[i:i+5]}')

    return scores