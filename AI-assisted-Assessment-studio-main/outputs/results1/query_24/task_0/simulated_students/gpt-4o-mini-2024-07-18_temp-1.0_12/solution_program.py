def board_game_summary(results):
    scores = {}
    i = 0
    n = len(results)

    while i < n:
        if i + 1 >= n or not results[i].isupper() or not results[i+1].isdigit():
            raise ValueError("Invalid format: Each player's score must be prefixed by their identifier and followed by a number.")

        player = results[i]
        j = i + 1

        while j < n and results[j].isdigit():
            j += 1

        score = int(results[i + 1:j])

        if player not in scores:
            scores[player] = 0
        scores[player] += score

        i = j

    return scores