def luckiest_player(filename):
    from collections import defaultdict
    winnings = defaultdict(int)
    
    with open(filename, 'r') as file:
        for line in file:
            name, amount = line.rsplit(' ', 1)
            winnings[name] += int(amount)
    
    max_winnings = -1
    luckiest_player = ''
    
    for player, total in winnings.items():
        if total > max_winnings or (total == max_winnings and player < luckiest_player):
            max_winnings = total
            luckiest_player = player
    
    return luckiest_player