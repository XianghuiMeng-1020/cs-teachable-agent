def luckiest_player(filename):
    winnings = {}
    
    with open(filename, 'r') as file:
        for line in file:
            player, amount = line.strip().split()
            amount = int(amount)
            if player in winnings:
                winnings[player] += amount
            else:
                winnings[player] = amount
    
    luckiest = None
    max_winnings = -1
    
    for player, total in winnings.items():
        if total > max_winnings or (total == max_winnings and (luckiest is None or player < luckiest)):
            luckiest = player
            max_winnings = total
    
    return luckiest