def find_winner(score_a, score_b):
    if score_a > score_b:
        return "Player A wins"
    elif score_b > score_a:
        return "Player B wins"
    else:
        return "Tie"

# Testing the function
print(find_winner(250, 150))  # Should return "Player A wins"
print(find_winner(100, 100))  # Should return "Tie"
print(find_winner(150, 250))  # Should return "Player B wins"
print(find_winner(-50, -100)) # Should return "Player A wins"
print(find_winner(-100, -50)) # Should return "Player B wins"