def board_game_summary(results):
    if not results:
        raise ValueError("Invalid format in results string")
    scores = {}
    i = 0
    while i < len(results):
        try:
            player = results[i]
            if not player.isupper() or i + 1 >= len(results):
                raise ValueError("Invalid format in results string")
            i += 1
            num_start = i
            while i < len(results) and results[i].isdigit():
                i += 1
            if num_start == i:
                raise ValueError("Invalid format in results string")
            score = int(results[num_start:i])
            if player in scores:
                scores[player] += score
            else:
                scores[player] = score
        except ValueError:
            raise ValueError("Invalid format in results string")
    return scores