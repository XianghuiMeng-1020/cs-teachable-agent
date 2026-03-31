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

    max_winnings = -1
    luckiest_player = None

    for name in winnings:
        total_winnings = winnings[name]
        if (total_winnings > max_winnings) or (total_winnings == max_winnings and (luckiest_player is None or name < luckiest_player)):
            max_winnings = total_winnings
            luckiest_player = name

    return luckiest_player