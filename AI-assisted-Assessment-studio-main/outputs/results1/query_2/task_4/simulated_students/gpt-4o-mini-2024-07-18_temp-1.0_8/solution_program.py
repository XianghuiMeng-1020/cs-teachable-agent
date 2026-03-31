def check_winner(log_file, player_name, lucky_number):
    player_name = player_name.lower().strip()
    lucky_number_str = str(lucky_number)

    with open(log_file, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) != 2:
                continue

            name = parts[0].lower()
            winning_number = parts[1]

            if name == player_name and winning_number == lucky_number_str:
                return True
    return False