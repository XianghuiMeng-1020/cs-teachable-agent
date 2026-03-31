def luckiest_player(filename):
    winnings = {}

    with open(filename, 'r') as file:
        for line in file:
            name, win = line.split()  # split the line into name and winnings
            win = int(win)  # convert winnings to integer

            if name in winnings:
                winnings[name] += win  # add winnings to the player's total
            else:
                winnings[name] = win  # initialize the player's winnings

    # Find the player with the maximum winnings
    luckiest = None
    max_winning = 0

    for player, total in winnings.items():
        if (total > max_winning) or (total == max_winning and (luckiest is None or player < luckiest)):
            luckiest = player
            max_winning = total

    return luckiest