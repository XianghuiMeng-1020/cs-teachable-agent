def simulate_lottery(player_numbers, rounds):
    # Check for valid player_numbers
    if not (isinstance(player_numbers, list) and len(player_numbers) == 6 and all(1 <= num <= 49 for num in player_numbers)):
        return 0
    
    # Initialize the count of wins
    win_count = 0
    
    # Iterate over each round to compare the player's numbers
    for round_key, winning_numbers in rounds.items():
        # Validate each round's winning numbers
        if not (isinstance(winning_numbers, list) and len(winning_numbers) == 6 and all(1 <= num <= 49 for num in winning_numbers)):
            return 0

        # Count common numbers between player and winning numbers
        common_numbers = set(player_numbers).intersection(winning_numbers)
        if len(common_numbers) >= 4:
            win_count += 1
    
    return win_count