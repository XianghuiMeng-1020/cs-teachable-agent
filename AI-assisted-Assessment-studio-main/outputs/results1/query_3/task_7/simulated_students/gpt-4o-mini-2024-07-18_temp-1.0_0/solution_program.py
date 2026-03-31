def simulate_lottery(player_numbers, rounds):
    if (len(player_numbers) != 6 or 
        not all(1 <= number <= 49 for number in player_numbers) or 
        len(set(player_numbers)) != 6):
        return 0
    
    total_wins = 0
    for round_number, winning_numbers in rounds.items():
        if (len(winning_numbers) != 6 or 
            not all(1 <= number <= 49 for number in winning_numbers) or 
            len(set(winning_numbers)) != 6):
            continue
        
        matched_numbers = len(set(player_numbers) & set(winning_numbers))
        if matched_numbers >= 4:
            total_wins += 1
    
    return total_wins