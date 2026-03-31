def check_winner(log_file, player_name, lucky_number):
    player_name = player_name.lower().strip()
    lucky_number = str(lucky_number)
    with open(log_file, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) != 2:
                continue
            name = parts[0].lower()
            number = parts[1]
            if name == player_name and number == lucky_number:
                return True
    return False