def calculate_score(moves):
    cumulative_score = 0
    for move in moves:
        if move.isdigit():
            value = int(move)
            if 1 <= value <= 6:
                cumulative_score += value
        elif move == 'skip':
            continue
    return cumulative_score