def simulate_lottery(player_numbers, rounds):
    if len(player_numbers) != 6 or any(n < 1 or n > 49 for n in player_numbers):
        return 0
    round_wins = 0
    for round_number, winning_numbers in rounds.items():
        if len(winning_numbers) != 6 or any(n < 1 or n > 49 for n in winning_numbers):
            continue
        matches = len(set(player_numbers) & set(winning_numbers))
        if matches >= 4:
            round_wins += 1
    return round_wins