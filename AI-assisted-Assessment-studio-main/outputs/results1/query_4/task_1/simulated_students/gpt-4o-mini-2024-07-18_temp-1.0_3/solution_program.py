def calculate_winnings(tosses):
    total_winnings = 0
    for toss in tosses:
        if toss == 'H':
            total_winnings += 2
        elif toss == 'T':
            total_winnings -= 1
    return total_winnings