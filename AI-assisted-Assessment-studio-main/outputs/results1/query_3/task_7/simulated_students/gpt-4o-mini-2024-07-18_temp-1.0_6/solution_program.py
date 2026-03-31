def simulate_lottery(player_numbers, rounds):
    if (len(player_numbers) != 6 or 
            any(not isinstance(num, int) or not (1 <= num <= 49) for num in player_numbers)):
        return 0

    win_count = 0

    for winning_numbers in rounds.values():
        if (len(winning_numbers) != 6 or 
                any(not isinstance(num, int) or not (1 <= num <= 49) for num in winning_numbers)):
            return 0

        matched_numbers = len(set(player_numbers) & set(winning_numbers))
        if matched_numbers >= 4:
            win_count += 1

    return win_count