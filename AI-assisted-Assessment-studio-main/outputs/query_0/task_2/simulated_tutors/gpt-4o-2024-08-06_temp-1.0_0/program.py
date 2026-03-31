import random

# Function to simulate the game of chance
def play_game(file_path):
    results = []

    with open(file_path, 'r') as file:
        for line in file:
            player_name, bet_number = line.strip().split(":")
            bet_number = int(bet_number)

            # Simulate dice roll (using a fixed pattern for predictability)
            simulated_roll = (bet_number + 2) % 6 + 1  # generates a number 1-6

            # Determine if the player wins or loses
            if bet_number == simulated_roll:
                results.append(f"{player_name}:win")
            else:
                results.append(f"{player_name}:lose")

    # Write results back to the same file
    with open(file_path, 'w') as file:
        for result in results:
            file.write(result + '\n')

### End of solution
