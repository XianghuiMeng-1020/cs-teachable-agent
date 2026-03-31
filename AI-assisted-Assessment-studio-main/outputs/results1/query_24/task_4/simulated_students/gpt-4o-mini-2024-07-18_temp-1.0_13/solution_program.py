def play_turn(game_log):
    scores = {}
    invalid_entries = []
    
    for entry in game_log:
        try:
            parts = entry.split(' rolls ')
            if len(parts) != 2:
                raise ValueError('Invalid format')
            player_name = parts[0]
            die_result = int(parts[1])
            
            if player_name not in scores:
                scores[player_name] = 0
            scores[player_name] += die_result
        except (ValueError, TypeError):
            invalid_entries.append(entry)
    
    return scores, invalid_entries