def play_turn(game_log):
    scores = {}
    invalid_entries = []
    
    for entry in game_log:
        try:
            player_name, _, die_result = entry.split()
            die_result = int(die_result)
            if player_name in scores:
                scores[player_name] += die_result
            else:
                scores[player_name] = die_result
        except (ValueError, IndexError):
            invalid_entries.append(entry)
    
    return scores, invalid_entries