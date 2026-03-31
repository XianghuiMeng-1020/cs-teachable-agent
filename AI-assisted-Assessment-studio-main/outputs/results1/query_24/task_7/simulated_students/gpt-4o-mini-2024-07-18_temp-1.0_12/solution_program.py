def calculate_score(moves):
    total_score = 0
    for move in moves:
        if move.isdigit() and 1 <= int(move) <= 6:
            total_score += int(move)
        elif move == 'skip':
            continue
        else:
            continue
    return total_score