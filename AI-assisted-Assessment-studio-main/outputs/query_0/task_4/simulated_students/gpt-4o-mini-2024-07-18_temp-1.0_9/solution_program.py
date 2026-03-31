def luckiest_player(filename):
    player_winnings = {}
    
    with open(filename, 'r') as file:
        for line in file:
            name, winnings = line.split()
            winnings = int(winnings)
            if name not in player_winnings:
                player_winnings[name] = 0
            player_winnings[name] += winnings
    
    max_winnings = -1
    luckiest_player = None
    
    for player, total in player_winnings.items():
        if total > max_winnings:
            max_winnings = total
            luckiest_player = player
        elif total == max_winnings:  
            if luckiest_player is None or player < luckiest_player:
                luckiest_player = player
    
    return luckiest_player