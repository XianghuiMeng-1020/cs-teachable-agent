def calculate_prize(roll1, roll2, roll3):
    if roll1 == roll2 == roll3:
        return roll1 * 10
    elif roll1 == roll2 or roll1 == roll3 or roll2 == roll3:
        return next(filter(lambda x: x in (roll1, roll2, roll3), [roll1, roll2, roll3])) * 5
    else:
        return roll1 + roll2 + roll3