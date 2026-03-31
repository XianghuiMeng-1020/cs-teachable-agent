def play_game_of_chance(board_positions, rolls):
    players_positions = {}
    
    for player, player_rolls in rolls.items():
        position = 0  # Each player starts at position 0
        for roll in player_rolls:
            position = (position + roll) % board_positions  # Update position with wrap-around
        players_positions[player] = position
        
    return players_positions

# Example usage
def main():
    result = play_game_of_chance(10, {'Alice': [3, 4, 2], 'Bob': [5, 2]})
    print(result)  # Output: {'Alice': 9, 'Bob': 7}

main()