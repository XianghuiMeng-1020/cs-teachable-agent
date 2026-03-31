def play_turn(game_log):
    scores = {}
    invalid_entries = []

    for entry in game_log:
        try:
            # Split the entry into components
            parts = entry.split()
            if len(parts) != 4 or parts[1] != 'rolls':
                raise ValueError('Invalid format')

            player_name = parts[0]
            die_result = int(parts[2])

            # Update the player's score
            if player_name not in scores:
                scores[player_name] = 0
            scores[player_name] += die_result

        except (ValueError, IndexError):
            # Capture any parsing errors or invalid die results
            invalid_entries.append(entry)

    return scores, invalid_entries