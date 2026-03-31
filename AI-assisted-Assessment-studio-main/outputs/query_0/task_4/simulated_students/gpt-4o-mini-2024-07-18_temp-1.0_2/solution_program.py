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

    max_winnings = -1
    max_player = None
    for player, total in winnings.items():
        if total > max_winnings:
            max_winnings = total
            max_player = player
        elif total == max_winnings:
            if max_player is None or player < max_player:
                max_player = player

    return max_player