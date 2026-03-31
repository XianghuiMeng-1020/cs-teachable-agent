def calculate_winnings(bets, roll):
    total_winnings = 0
    for number, amount in bets.items():
        if number == roll:
            total_winnings += amount * 3
        else:
            total_winnings -= amount
    return total_winnings

# Example usage
print(calculate_winnings({1: 10, 2: 20, 3: 0, 4: 15, 5: 5, 6: 0}, 3))  # Output: -50