def pantheon_oracle(adventure_logs):
    fortune = 0
    count = 1
    n = len(adventure_logs)
  
    for i in range(1, n):
        if adventure_logs[i] == adventure_logs[i - 1]:
            count += 1
        else:
            if count == 3:
                fortune += 10
            elif count == 7:
                fortune += 30
            elif count == 2:
                fortune -= 5
            count = 1

    if count == 3:
        fortune += 10
    elif count == 7:
        fortune += 30
    elif count == 2:
        fortune -= 5

    return fortune
