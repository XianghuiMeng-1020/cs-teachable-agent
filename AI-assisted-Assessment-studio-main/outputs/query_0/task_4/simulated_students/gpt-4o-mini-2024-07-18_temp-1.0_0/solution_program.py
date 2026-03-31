def luckiest_player(filename):
    # Dictionary to hold player winnings
    winnings = {}

    # Read the file and accumulate winnings
    with open(filename, 'r') as file:
        for line in file:
            name, amount = line.split()  # Split the line into name and winnings
            amount = int(amount)  # Convert winnings to integer

            # Accumulate winnings for each player
            if name in winnings:
                winnings[name] += amount
            else:
                winnings[name] = amount

    # Determine the player with the maximum winnings, with a tie-breaking rule
    luckiest_player = None
    max_winnings = -1

    for player, total in winnings.items():
        if (total > max_winnings) or (total == max_winnings and (luckiest_player is None or player < luckiest_player)):
            max_winnings = total
            luckiest_player = player

    return luckiest_player