def calculate_winnings(tosses):
    winnings = 0
    for toss in tosses:
        if toss == 'H':
            winnings += 2
        elif toss == 'T':
            winnings -= 1
    return winnings