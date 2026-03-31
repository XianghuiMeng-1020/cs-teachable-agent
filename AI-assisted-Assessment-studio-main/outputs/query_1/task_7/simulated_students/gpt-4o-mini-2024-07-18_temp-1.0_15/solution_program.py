def maximize_favor(challenges):
    n = len(challenges)
    dp = [[0] * (11) for _ in range(n + 1)]

    for i in range(1, n + 1):
        reward, difficulty = challenges[i - 1]
        for j in range(11):
            dp[i][j] = dp[i - 1][j]  # Not picking the challenge
            if j >= difficulty:
                dp[i][j] = max(dp[i][j], dp[i - 1][j - difficulty] + reward)  # Picking the challenge

    return dp[n][10]