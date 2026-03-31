def calculate_score(moves):
    cumulative_score = 0
    for move in moves:
        if move == 'skip':
            continue
        try:
            roll = int(move)
            if 1 <= roll <= 6:
                cumulative_score += roll
        except ValueError:
            continue
    return cumulative_score