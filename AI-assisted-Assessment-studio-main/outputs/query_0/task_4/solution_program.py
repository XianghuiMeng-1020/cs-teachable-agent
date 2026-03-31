def luckiest_player(filename):
    with open(filename, 'r') as file:
        player_totals = {}
        for line in file:
            name, winnings = line.rsplit(maxsplit=1)
            winnings = int(winnings)
            if name in player_totals:
                player_totals[name] += winnings
            else:
                player_totals[name] = winnings
        max_winnings = -float('inf')
        luckiest = None
        for player in sorted(player_totals):
            if player_totals[player] > max_winnings:
                max_winnings = player_totals[player]
                luckiest = player
        return luckiest
