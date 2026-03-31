def check_dice_lottery_results(results):
    # List to store results of each dice roll
    lottery_results = []
    
    # Iterate through each pair of dice results
    for result in results:
        # Extract individual dice values
        die1, die2 = result
        # Calculate sum of dice
        total = die1 + die2
        
        # Determine if the current roll is a winning roll
        if (total == 7) or (total == 11):
            lottery_results.append(True)
        elif die1 == die2 and total > 8:
            lottery_results.append(True)
        else:
            lottery_results.append(False)
    
    return lottery_results

# Example usage
print(check_dice_lottery_results([(1, 6), (3, 4), (2, 2), (6, 6), (5, 6)]))
# Outputs: [True, True, False, True, False]