def simulate_lottery(player_numbers, rounds):
    if (len(player_numbers) != 6 or 
        any(n < 1 or n > 49 for n in player_numbers) or 
        len(set(player_numbers)) != 6):
        return 0
    win_count = 0
    for round_number, winning_numbers in rounds.items():
        if (len(winning_numbers) != 6 or 
            any(n < 1 or n > 49 for n in winning_numbers) or 
            len(set(winning_numbers)) != 6):
            return 0
        matches = len(set(player_numbers) & set(winning_numbers))
        if matches >= 4:
            win_count += 1
    return win_count