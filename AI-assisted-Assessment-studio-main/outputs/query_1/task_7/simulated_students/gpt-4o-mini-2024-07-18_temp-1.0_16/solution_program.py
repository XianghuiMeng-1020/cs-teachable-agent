def maximize_favor(challenges):
    n = len(challenges)
    dp = [0] * 11

    for reward, difficulty in challenges:
        for i in range(10, difficulty - 1, -1):
            dp[i] = max(dp[i], dp[i - difficulty] + reward)

    return max(dp)