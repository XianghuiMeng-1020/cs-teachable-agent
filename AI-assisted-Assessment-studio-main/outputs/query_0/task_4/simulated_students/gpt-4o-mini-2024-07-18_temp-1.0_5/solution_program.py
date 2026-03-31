def luckiest_player(filename):
    winnings = {}

    with open(filename, 'r') as file:
        for line in file:
            name, win = line.split()
            win = int(win)
            if name in winnings:
                winnings[name] += win
            else:
                winnings[name] = win

    max_winnings = -1
    luckiest_player = None

    for player, total in winnings.items():
        if total > max_winnings:
            max_winnings = total
            luckiest_player = player
        elif total == max_winnings:
            if luckiest_player is None or player < luckiest_player:
                luckiest_player = player

    return luckiest_player