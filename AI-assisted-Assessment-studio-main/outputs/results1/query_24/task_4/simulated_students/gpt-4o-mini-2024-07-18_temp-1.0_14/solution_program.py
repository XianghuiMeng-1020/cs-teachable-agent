def play_turn(game_log):
    scores = {}
    invalid_entries = []
    
    for event in game_log:
        try:
            parts = event.split(' rolls ')
            if len(parts) != 2:
                raise ValueError('Invalid format')
            player_name = parts[0]
            die_result = int(parts[1])
            if player_name in scores:
                scores[player_name] += die_result
            else:
                scores[player_name] = die_result
        except (ValueError, TypeError):
            invalid_entries.append(event)
    
    return (scores, invalid_entries)