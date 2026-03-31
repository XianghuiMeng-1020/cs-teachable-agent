def calculate_prize(roll1, roll2, roll3):
    if roll1 == roll2 == roll3:
        return roll1 * 10
    elif roll1 == roll2 or roll1 == roll3:
        return roll1 * 5
    elif roll2 == roll3:
        return roll2 * 5
    else:
        return roll1 + roll2 + roll3

# Sample tests
print(calculate_prize(4, 4, 4))  # Should return 40
print(calculate_prize(3, 3, 2))  # Should return 15
print(calculate_prize(1, 2, 3))  # Should return 6