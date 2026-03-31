def dice_probability(target_score):
    # Define the total number of possible outcomes when rolling two dice
    total_outcomes = 36
    
    # Check if the target score is out of bounds
    if target_score < 2 or target_score > 12:
        return 0

    # Define a dictionary to count the number of favorable outcomes for each possible score
    score_counts = {i: 0 for i in range(2, 13)}
    
    # Use nested loops to simulate rolling two dice
    for die1 in range(1, 7):
        for die2 in range(1, 7):
            score = die1 + die2
            if score in score_counts:
                score_counts[score] += 1

    # Calculate the probability for the target score
    favorable_outcomes = score_counts[target_score]
    probability = favorable_outcomes / total_outcomes
    
    return round(probability, 4)

# The function should be tested with the provided test suite to ensure correctness.