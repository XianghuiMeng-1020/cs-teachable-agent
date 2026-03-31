def luckiest_player(filename):
    with open(filename, 'r') as file:
        winnings = {}
        for line in file:
            name, amount = line.strip().split()
            amount = int(amount)
            if name in winnings:
                winnings[name] += amount
            else:
                winnings[name] = amount

    max_winnings = -1
    luckiest_player = None
    for player, total in winnings.items():
        if total > max_winnings or (total == max_winnings and (luckiest_player is None or player < luckiest_player)):
            max_winnings = total
            luckiest_player = player

    return luckiest_player