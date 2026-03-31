def maximize_favor(challenges):
    n = len(challenges)
    dp = [0] * 11  # dp[i] will be the max reward for difficulty i

    for reward, difficulty in challenges:
        for j in range(10, difficulty - 1, -1):  # iterate difficulty from 10 to difficulty
            dp[j] = max(dp[j], dp[j - difficulty] + reward)

    return max(dp)