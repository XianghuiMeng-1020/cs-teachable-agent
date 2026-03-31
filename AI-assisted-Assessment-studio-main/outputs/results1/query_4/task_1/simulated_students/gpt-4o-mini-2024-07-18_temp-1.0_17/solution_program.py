def calculate_winnings(tosses):
    total = 0
    for toss in tosses:
        if toss == 'H':
            total += 2
        elif toss == 'T':
            total -= 1
    return total