def luckiest_player(filename):
    winnings = {}
    with open(filename, 'r') as file:
        for line in file:
            name, amount = line.strip().split()
            amount = int(amount)
            if name in winnings:
                winnings[name] += amount
            else:
                winnings[name] = amount
    max_winner = None
    max_amount = -1
    for player, total in winnings.items():
        if total > max_amount:
            max_amount = total
            max_winner = player
        elif total == max_amount:
            if player < max_winner:
                max_winner = player
    return max_winner