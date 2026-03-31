def maximize_favor(challenges):
    n = len(challenges)
    dp = [0] * 11  # Initialize a DP array for difficulties up to 10

    for reward, difficulty in challenges:
        # Iterate backwards to avoid using the same item multiple times
        for j in range(10, difficulty - 1, -1):
            dp[j] = max(dp[j], dp[j - difficulty] + reward)

    return max(dp)