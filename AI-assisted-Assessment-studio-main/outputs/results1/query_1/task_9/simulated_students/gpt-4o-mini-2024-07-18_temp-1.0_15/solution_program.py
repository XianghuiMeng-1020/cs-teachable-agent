def calculate_prize(roll1, roll2, roll3):
    if roll1 == roll2 == roll3:
        return roll1 * 10
    elif roll1 == roll2 or roll1 == roll3 or roll2 == roll3:
        return (roll1 if roll1 == roll2 or roll1 == roll3 else roll2) * 5
    else:
        return roll1 + roll2 + roll3