def play_turn(game_log):
    scores = {}
    invalid_entries = []

    for entry in game_log:
        try:
            player, _, die_result = entry.split()
            die_result = int(die_result)
            if player not in scores:
                scores[player] = 0
            scores[player] += die_result
        except (ValueError, IndexError):
            invalid_entries.append(entry)

    return scores, invalid_entries