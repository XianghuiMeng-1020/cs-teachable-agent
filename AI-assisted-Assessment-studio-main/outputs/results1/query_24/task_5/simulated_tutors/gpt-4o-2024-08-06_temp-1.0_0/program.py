def calculate_final_score(moves):
    position = 0
    for move in moves.split(','):
        try:
            roll = int(move)
            if 1 <= roll <= 6:
                if position + roll <= 100:
                    position += roll
        except ValueError:
            continue  # Skip invalid entries
    return position