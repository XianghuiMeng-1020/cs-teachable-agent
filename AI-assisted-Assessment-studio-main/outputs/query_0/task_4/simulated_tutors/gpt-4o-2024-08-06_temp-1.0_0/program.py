def luckiest_player(filename):
    player_winnings = {}
    
    # Reading file and processing winnings
    with open(filename, 'r') as file:
        for line in file:
            name, winnings = line.split()
            winnings = int(winnings)
            
            if name in player_winnings:
                player_winnings[name] += winnings
            else:
                player_winnings[name] = winnings
    
    # Finding the luckiest player
    luckiest, max_winnings = '', float('-inf')
    for player, total_winnings in sorted(player_winnings.items()):
        if total_winnings > max_winnings:
            luckiest, max_winnings = player, total_winnings
    
    return luckiest