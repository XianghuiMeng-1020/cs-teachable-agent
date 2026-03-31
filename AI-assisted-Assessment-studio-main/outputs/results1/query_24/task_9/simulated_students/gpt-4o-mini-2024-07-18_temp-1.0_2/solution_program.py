def calculate_score(position, rolls):
    if position < 0:
        raise ValueError("Position cannot be negative.")
    if any(not(1 <= roll <= 6) for roll in rolls):
        raise ValueError("All rolls must be between 1 and 6.")
    rolls_sum = sum(rolls)
    new_position = position + rolls_sum
    score = new_position * 10
    return score