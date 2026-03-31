def maximize_favor(challenges):
    # Number of challenges
    n = len(challenges)
    # Maximum difficulty allowed
    max_difficulty = 10
    
    # Create a DP array to store the maximum reward at each level of difficulty
    dp = [0] * (max_difficulty + 1)
    
    # Process each challenge
    for reward, difficulty in challenges:
        # Update the dp array from back to front to avoid overwriting
        for d in range(max_difficulty, difficulty - 1, -1):
            dp[d] = max(dp[d], dp[d - difficulty] + reward)
    
    # The maximum divine reward is the maximum value in dp array
    return max(dp)