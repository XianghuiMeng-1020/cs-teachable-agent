def play_turn(game_log):
    scores = {}
    invalid_entries = []

    for entry in game_log:
        try:
            parts = entry.split()
            if len(parts) != 4 or parts[1] != 'rolls':
                raise ValueError('Invalid format')
            player_name = parts[0]
            die_result = int(parts[2])  # This can raise ValueError if not an integer

            if player_name not in scores:
                scores[player_name] = 0
            scores[player_name] += die_result

        except Exception:
            invalid_entries.append(entry)

    return scores, invalid_entries