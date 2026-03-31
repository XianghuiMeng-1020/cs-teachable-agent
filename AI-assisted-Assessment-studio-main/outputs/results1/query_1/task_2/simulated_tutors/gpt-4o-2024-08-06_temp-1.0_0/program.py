def spin_wheel(bet_list, target_number):
    total_winnings = 0
    
    for bet_number, bet_amount in bet_list:
        if bet_number == target_number:  # Selection Statement
            total_winnings += bet_amount * 10  # Arithmetic Operator
            
    return total_winnings

# Example usage
bets = [(5, 10), (12, 20), (18, 5)]
target = 7
print(spin_wheel(bets, target))  # Output should be 0 as there is no match