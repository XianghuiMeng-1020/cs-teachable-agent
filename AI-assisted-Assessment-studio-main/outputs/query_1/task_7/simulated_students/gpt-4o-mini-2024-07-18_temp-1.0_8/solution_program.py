def maximize_favor(challenges):
    n = len(challenges)
    max_difficulty = 10
    dp = [0] * (max_difficulty + 1)
    
    for reward, difficulty in challenges:
        for j in range(max_difficulty, difficulty - 1, -1):
            dp[j] = max(dp[j], dp[j - difficulty] + reward)
    
    return dp[max_difficulty]