def lucky_dice(outcomes):
    # Initialize total score and list to hold individual roll scores
    total_score = 0
    roll_scores = []
    
    # Loop over each outcome tuple in the outcomes list
    for roll in outcomes:
        # Calculate the sum of the two dice
        dice_sum = roll[0] + roll[1]

        # Determine the score based on the sum of the dice
        if dice_sum in [7, 11]:
            score = 10
        elif dice_sum in [2, 3, 12]:
            score = 5
        else:
            score = 0

        # Append the score to the roll_scores list
        roll_scores.append(score)
        # Add the score to the total score
        total_score += score

    # Return the results as a dictionary
    return {
        'total_score': total_score,
        'rolls': roll_scores
    }