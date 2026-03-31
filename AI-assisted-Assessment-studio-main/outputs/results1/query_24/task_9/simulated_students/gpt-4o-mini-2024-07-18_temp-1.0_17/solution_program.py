def calculate_score(position, rolls):
    if position < 0:
        raise ValueError("Position cannot be negative.")
    for roll in rolls:
        if roll < 1 or roll > 6:
            raise ValueError("All rolls must be between 1 and 6.")
    sum_of_rolls = sum(rolls)
    new_position = position + sum_of_rolls
    score = new_position * 10
    return score