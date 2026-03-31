def check_winner(log_file, player_name, lucky_number):
    player_name = player_name.strip().lower()  # Ensure the player name is case insensitive
    lucky_number = str(lucky_number)  # Convert the lucky number to string for comparison
    
    with open(log_file, 'r') as file:
        for line in file:
            # Split the line into name and number, remove any extra spaces
            current_name, winning_number = line.strip().split()
            
            # Check if case-normalized name matches and number matches
            if current_name.lower() == player_name and winning_number == lucky_number:
                return True  # Winner found
    return False  # No matching winner found