def simulate_lottery(player_numbers, rounds):
    if len(player_numbers) != 6 or any(not (1 <= num <= 49) for num in player_numbers):
        return 0
    wins = 0
    for round_number, winning_numbers in rounds.items():
        if len(winning_numbers) != 6 or any(not (1 <= num <= 49) for num in winning_numbers):
            continue
        matched_numbers = 0
        for number in player_numbers:
            if number in winning_numbers:
                matched_numbers += 1
        if matched_numbers >= 4:
            wins += 1
    return wins