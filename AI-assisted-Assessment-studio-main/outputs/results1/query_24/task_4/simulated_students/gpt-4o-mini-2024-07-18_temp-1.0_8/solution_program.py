def play_turn(game_log):
    scores = {}
    invalid_entries = []

    for entry in game_log:
        try:
            parts = entry.split()  # Split the entry on whitespace
            player_name = parts[0]  # The first part is the player name
            die_result = int(parts[2])  # The die result is the third part (as integer)

            # Update the scores dictionary
            if player_name in scores:
                scores[player_name] += die_result
            else:
                scores[player_name] = die_result
        except (IndexError, ValueError):  # Handle index errors and value errors
            invalid_entries.append(entry)  # Add invalid entry if an exception occurs

    return (scores, invalid_entries)