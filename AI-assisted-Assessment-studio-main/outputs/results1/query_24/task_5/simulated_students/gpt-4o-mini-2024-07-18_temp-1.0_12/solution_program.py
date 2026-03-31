def calculate_final_score(moves):
    moves_list = moves.split(',')
    score = 0
    for move in moves_list:
        try:
            roll = int(move)
            if 1 <= roll <= 6:
                if score + roll <= 100:
                    score += roll
        except ValueError:
            continue
    return score