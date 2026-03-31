def calculate_final_score(moves):
    current_position = 0
    try:
        rolls = moves.split(",")
        for roll in rolls:
            try:
                step = int(roll)
                if 1 <= step <= 6:
                    if current_position + step <= 100:
                        current_position += step
            except ValueError:
                continue
    except Exception:
        return current_position
    return current_position