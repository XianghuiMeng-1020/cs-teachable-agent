def tally_scores(file_path):
    players = {}
    with open(file_path, 'r') as f:
        for line in f:
            player, score = line.strip().split(':')
            score = int(score)
            if player in players:
                players[player] += score
            else:
                players[player] = score
    result = [(player, total) for player, total in players.items()]
    result.sort(key=lambda x: (-x[1], x[0]))
    return result