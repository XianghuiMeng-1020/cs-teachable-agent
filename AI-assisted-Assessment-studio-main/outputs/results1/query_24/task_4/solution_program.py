def play_turn(game_log):
    scores = {}
    invalid_entries = []
    for entry in game_log:
        try:
            parts = entry.split()
            player = parts[0]
            roll_action = parts[1].lower()
            roll_value = int(parts[2])
            if roll_action != 'rolls':
                raise ValueError

            if player in scores:
                scores[player] += roll_value
            else:
                scores[player] = roll_value
        except (IndexError, ValueError):
            invalid_entries.append(entry)
    return scores, invalid_entries
