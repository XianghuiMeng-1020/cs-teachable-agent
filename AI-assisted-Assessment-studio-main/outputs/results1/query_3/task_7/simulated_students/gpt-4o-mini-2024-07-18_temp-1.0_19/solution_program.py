def simulate_lottery(player_numbers, rounds):
    if (len(player_numbers) != 6 or 
        any(num < 1 or num > 49 for num in player_numbers) or 
        len(set(player_numbers)) != 6):
        return 0

    wins = 0
    for round_numbers in rounds.values():
        if (len(round_numbers) != 6 or 
            any(num < 1 or num > 49 for num in round_numbers) or 
            len(set(round_numbers)) != 6):
            return 0

        match_count = len(set(player_numbers) & set(round_numbers))
        if match_count >= 4:
            wins += 1

    return wins