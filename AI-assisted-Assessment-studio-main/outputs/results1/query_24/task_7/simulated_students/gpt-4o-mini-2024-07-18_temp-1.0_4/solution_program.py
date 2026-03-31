def calculate_score(moves):
    total_score = 0
    for move in moves:
        if move == 'skip':
            continue
        try:
            roll = int(move)
            if 1 <= roll <= 6:
                total_score += roll
        except ValueError:
            continue
    return total_score