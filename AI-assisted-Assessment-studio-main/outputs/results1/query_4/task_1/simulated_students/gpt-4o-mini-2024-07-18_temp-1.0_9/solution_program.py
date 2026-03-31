def calculate_winnings(tosses):
    total = 0
    for result in tosses:
        if result == 'H':
            total += 2
        elif result == 'T':
            total -= 1
    return total