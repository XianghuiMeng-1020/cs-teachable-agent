def simulate_lottery(player_numbers, rounds):
    if len(player_numbers) != 6 or any(n < 1 or n > 49 for n in player_numbers):
        return 0

    player_set = set(player_numbers)
    rounds_won = 0

    for round_number, winning_numbers in rounds.items():
        if len(winning_numbers) != 6 or any(n < 1 or n > 49 for n in winning_numbers):
            return 0
        winning_set = set(winning_numbers)
        matched_numbers = player_set.intersection(winning_set)
        if len(matched_numbers) >= 4:
            rounds_won += 1

    return rounds_won