def dice_game(target_score, rolls):
    total_score = 0  # Initialize the total score
    
    # Iterate over each roll
    for roll in rolls:
        total_score += roll  # Add the roll value to the total score
        
        # Check if the total score reached or exceeded the target score
        if total_score >= target_score:
            return 'WIN'
            
    # If loop completes and target isn't met, the player loses
    return 'LOSE'

# After implementing the function, 
# you would place the given test cases in a separate test file, and use pytest to test the implementation.