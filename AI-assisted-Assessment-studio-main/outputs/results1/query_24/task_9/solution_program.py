def calculate_score(position, rolls):
    if position < 0:
        raise ValueError("Invalid starting position")
    for roll in rolls:
        if roll < 1 or roll > 6:
            raise ValueError("Invalid roll number")
    total_roll = 0
    for roll in rolls:
        total_roll += roll
    new_position = position + total_roll
    score = new_position * 10
    return score