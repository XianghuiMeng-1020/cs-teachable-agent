def maximize_favor(challenges):
    n = len(challenges)
    max_diff = 10
    dp = [0] * (max_diff + 1)

    for reward, difficulty in challenges:
        for j in range(max_diff, difficulty - 1, -1):
            dp[j] = max(dp[j], dp[j - difficulty] + reward)

    return max(dp)