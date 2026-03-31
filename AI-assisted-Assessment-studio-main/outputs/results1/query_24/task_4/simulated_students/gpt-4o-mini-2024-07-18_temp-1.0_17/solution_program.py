def play_turn(game_log):
    scores = {}
    invalid_entries = []

    for event in game_log:
        try:
            # Split the event into parts
            parts = event.split()
            if len(parts) != 4 or parts[1] != 'rolls':
                raise ValueError('Invalid format')
            player_name = parts[0]
            die_result = int(parts[2])

            # Update the score of the player
            if player_name not in scores:
                scores[player_name] = 0
            scores[player_name] += die_result
        except (ValueError, IndexError):
            invalid_entries.append(event)

    return (scores, invalid_entries)