def luckiest_player(filename):
    from collections import defaultdict
    
    winnings = defaultdict(int)
    
    with open(filename, 'r') as file:
        for line in file:
            name, amount = line.rsplit(' ', 1)
            winnings[name] += int(amount)
    
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