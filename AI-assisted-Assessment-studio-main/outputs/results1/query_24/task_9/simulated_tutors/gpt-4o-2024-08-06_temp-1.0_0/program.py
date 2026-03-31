def calculate_score(position, rolls):
    # Check for invalid initial position
    if position < 0:
        raise ValueError("Position cannot be negative")
    
    # Verify all dice rolls are valid
    for roll in rolls:
        if roll < 1 or roll > 6:
            raise ValueError("Rolls must be between 1 and 6")
    
    # Calculate the sum of the dice rolls
    sum_of_rolls = sum(rolls)
    
    # Determine the new position
    new_position = position + sum_of_rolls
    
    # Calculate the score
    score = new_position * 10
    
    return score