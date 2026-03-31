def simulate_lottery(player_numbers, rounds):
    if (len(player_numbers) != 6 or
        any(num < 1 or num > 49 for num in player_numbers) or
        len(set(player_numbers)) != 6):
        return 0

    total_wins = 0
    for round_number, winning_numbers in rounds.items():
        if (len(winning_numbers) != 6 or
            any(num < 1 or num > 49 for num in winning_numbers) or
            len(set(winning_numbers)) != 6):
            continue

        matches = len(set(player_numbers) & set(winning_numbers))
        if matches >= 4:
            total_wins += 1

    return total_wins