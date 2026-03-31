def simulate_lottery(player_numbers, rounds):
    if (len(player_numbers) != 6 or 
        any(num < 1 or num > 49 for num in player_numbers) or 
        len(rounds) == 0 or 
        any(len(winning_numbers) != 6 or 
            any(num < 1 or num > 49 for num in winning_numbers) for winning_numbers in rounds.values())):
        return 0

    win_count = 0
    for winning_numbers in rounds.values():
        matching_numbers = set(player_numbers).intersection(set(winning_numbers))
        if len(matching_numbers) >= 4:
            win_count += 1

    return win_count