def maximize_favor(challenges):
    max_difficulty = 10
    num_challenges = len(challenges)
    dp = [0] * (max_difficulty + 1)

    for reward, difficulty in challenges:
        for d in range(max_difficulty, difficulty - 1, -1):
            dp[d] = max(dp[d], dp[d - difficulty] + reward)

    return max(dp)