def determine_turn_winner(player_1_name, player_1_score, player_2_name, player_2_score):
    if player_1_score > player_2_score:
        return player_1_name
    elif player_2_score > player_1_score:
        return player_2_name
    else:
        return "Draw"

# Example usage of the function:
print(determine_turn_winner("Alice", 85, "Bob", 90))  # Output "Bob"
print(determine_turn_winner("Alice", 50, "Bob", 50))  # Output "Draw"