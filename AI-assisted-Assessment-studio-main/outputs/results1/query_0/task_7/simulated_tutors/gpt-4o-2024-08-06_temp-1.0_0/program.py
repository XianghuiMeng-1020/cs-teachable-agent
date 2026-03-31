def game_of_chance(filename):
    # Initial score
    score = 10
    
    # Placeholder to store the bet amount
    current_bet = 0
    
    # Open the input file and process each line
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            
            for line in lines:
                line = line.strip()

                # If the line is a digit, treat it as a bet amount
                if line.isdigit():
                    current_bet = int(line)
                
                # If the line is an action, execute the action with the current bet
                elif line in ['win', 'lose', 'draw']:
                    if line == 'win':
                        score += current_bet
                    elif line == 'lose':
                        # Ensure player has enough score to bet
                        if current_bet <= score:
                            score -= current_bet
                    # Draw is a no-op, no change to score

    except FileNotFoundError:
        print("The file was not found.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    # Write the final score to result.txt
    with open('result.txt', 'w') as result_file:
        result_file.write(str(score))