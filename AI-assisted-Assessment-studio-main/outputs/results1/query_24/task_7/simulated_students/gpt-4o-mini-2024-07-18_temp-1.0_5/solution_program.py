def calculate_score(moves):
    total_score = 0
    for move in moves:
        if move == 'skip':
            continue
        try:
            value = int(move)
            if 1 <= value <= 6:
                total_score += value
        except ValueError:
            continue
    return total_score