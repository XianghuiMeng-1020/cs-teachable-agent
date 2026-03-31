def play_turn(game_log):
    scores = {}
    invalid_entries = []

    for entry in game_log:
        try:
            player_name, _, die_result = entry.split()
            die_result = int(die_result)
            if player_name not in scores:
                scores[player_name] = 0
            scores[player_name] += die_result
        except:
            invalid_entries.append(entry)

    return (scores, invalid_entries)