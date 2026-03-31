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

    luckiest_player = None
    max_winnings = -1

    for player, total in winnings.items():
        if total > max_winnings:
            max_winnings = total
            luckiest_player = player
        elif total == max_winnings:
            if luckiest_player is None or player < luckiest_player:
                luckiest_player = player

    return luckiest_player