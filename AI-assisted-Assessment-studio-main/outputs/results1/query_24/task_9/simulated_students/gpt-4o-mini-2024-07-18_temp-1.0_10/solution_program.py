def calculate_score(position, rolls):
    if position < 0:
        raise ValueError("Position cannot be negative.")
    if any(roll < 1 or roll > 6 for roll in rolls):
        raise ValueError("Rolls must be between 1 and 6.")
    total_roll = sum(rolls)
    new_position = position + total_roll
    score = new_position * 10
    return score