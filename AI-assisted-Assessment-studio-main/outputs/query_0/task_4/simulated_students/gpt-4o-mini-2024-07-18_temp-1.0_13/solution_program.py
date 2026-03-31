def luckiest_player(filename):
    winnings = {}
    with open(filename, 'r') as file:
        for line in file:
            name, amount = line.split()
            amount = int(amount)
            if name in winnings:
                winnings[name] += amount
            else:
                winnings[name] = amount
    # Determine the luckiest player
    luckiest = None
    max_winnings = -1
    for player, total in winnings.items():
        if total > max_winnings:
            luckiest = player
            max_winnings = total
        elif total == max_winnings:
            if player < luckiest:
                luckiest = player
    return luckiest