def calculate_score(moves):
    total_score = 0
    for move in moves:
        try:
            if move.isdigit() and 1 <= int(move) <= 6:
                total_score += int(move)
        except:
            continue
    return total_score