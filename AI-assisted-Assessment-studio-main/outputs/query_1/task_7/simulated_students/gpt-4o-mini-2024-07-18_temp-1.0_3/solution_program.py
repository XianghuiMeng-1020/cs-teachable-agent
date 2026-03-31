def maximize_favor(challenges):
    max_difficulty = 10
    n = len(challenges)
    dp = [0] * (max_difficulty + 1)

    for reward, difficulty in challenges:
        for j in range(max_difficulty, difficulty - 1, -1):
            dp[j] = max(dp[j], dp[j - difficulty] + reward)

    return dp[max_difficulty]