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

    # Find the player with the highest winnings
    max_winnings = -1
    luckiest_player = None

    for player, total in winnings.items():
        if (total > max_winnings) or (total == max_winnings and (luckiest_player is None or player < luckiest_player)):
            max_winnings = total
            luckiest_player = player

    return luckiest_player