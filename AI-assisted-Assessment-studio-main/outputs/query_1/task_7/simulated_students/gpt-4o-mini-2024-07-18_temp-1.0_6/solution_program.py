def maximize_favor(challenges):
    n = len(challenges)
    max_difficulty = 10
    # Create a DP array to store the maximum reward for each difficulty level
    dp = [0] * (max_difficulty + 1)

    # Process each challenge
    for reward, difficulty in challenges:
        for d in range(max_difficulty, difficulty - 1, -1):
            dp[d] = max(dp[d], dp[d - difficulty] + reward)

    return dp[max_difficulty]