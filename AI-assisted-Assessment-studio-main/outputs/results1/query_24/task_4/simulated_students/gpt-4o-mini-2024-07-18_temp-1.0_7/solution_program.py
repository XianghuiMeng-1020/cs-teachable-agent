def play_turn(game_log):
    scores = {}
    invalid_entries = []

    for entry in game_log:
        try:
            # Split the entry into components
            parts = entry.split()
            if len(parts) != 4 or parts[1] != 'rolls':
                raise ValueError('Invalid format')

            player = parts[0]
            die_result = int(parts[2])

            # Update player score in the dictionary
            if player in scores:
                scores[player] += die_result
            else:
                scores[player] = die_result

        except (ValueError, IndexError):
            invalid_entries.append(entry)

    return (scores, invalid_entries)