def maximize_favor(challenges):
    # Initialize DP table
    dp = [0] * 11  # As max difficulty the hero can face is 10

    # Process each challenge
    for reward, difficulty in challenges:
        # Update DP table in reverse to prevent reuse of the same challenge
        for current_difficulty in range(10, difficulty - 1, -1):
            dp[current_difficulty] = max(dp[current_difficulty], dp[current_difficulty - difficulty] + reward)

    # The maximum achievable reward with the allowed difficulty
    return dp[10]