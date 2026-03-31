def maximize_favor(challenges):
    max_favor = 0
    n = len(challenges)
    for i in range(1 << n):
        total_reward = 0
        total_difficulty = 0
        for j in range(n):
            if (i & (1 << j)) != 0:
                total_reward += challenges[j][0]
                total_difficulty += challenges[j][1]
        if total_difficulty <= 10:
            max_favor = max(max_favor, total_reward)
    return max_favor
