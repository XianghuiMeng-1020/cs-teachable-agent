def calculate_score(moves):
    score = 0
    for move in moves:
        if move == 'skip':
            continue
        try:
            roll = int(move)
            if 1 <= roll <= 6:
                score += roll
        except ValueError:
            continue
    return score