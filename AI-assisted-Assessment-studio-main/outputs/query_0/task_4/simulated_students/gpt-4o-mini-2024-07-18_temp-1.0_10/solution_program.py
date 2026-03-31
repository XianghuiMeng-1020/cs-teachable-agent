def luckiest_player(filename):
    winnings = {}

    # Read the file and calculate total winnings for each player
    with open(filename, 'r') as file:
        for line in file:
            name, amount = line.rsplit(' ', 1)
            amount = int(amount)
            if name in winnings:
                winnings[name] += amount
            else:
                winnings[name] = amount

    # Determine the luckiest player
    luckiest_player = None
    max_winnings = -1

    for player, total in winnings.items():
        # Find the player with max winnings or first alphabetically in tie
        if total > max_winnings or (total == max_winnings and (luckiest_player is None or player < luckiest_player)):
            luckiest_player = player
            max_winnings = total

    return luckiest_player