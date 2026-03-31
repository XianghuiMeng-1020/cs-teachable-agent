def luckiest_player(filename):
    winnings = {}
    with open(filename, 'r') as file:
        for line in file:
            name, amount = line.strip().rsplit(' ', 1)
            amount = int(amount)
            if name in winnings:
                winnings[name] += amount
            else:
                winnings[name] = amount
    max_winning = -1
    luckiest_player = None
    for player in sorted(winnings.keys()):
        if winnings[player] > max_winning:
            max_winning = winnings[player]
            luckiest_player = player
    return luckiest_player