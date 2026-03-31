def play_game_of_chance(file_name, bet_amount, bet_guess):
    # Initialize winnings
    total_winnings = 0
    
    # Open the file and process each line
    with open(file_name, 'r') as file:
        for line in file:
            winning_number = int(line.strip())  # Convert line to integer
            
            # Check if the bet_guess matches the winning number
            if bet_guess == winning_number:
                # Player wins double the bet_amount for each match
                total_winnings += bet_amount * 2

    # Calculate net balance (subtract the initial bet_amount)
    balance = total_winnings - bet_amount

    return balance