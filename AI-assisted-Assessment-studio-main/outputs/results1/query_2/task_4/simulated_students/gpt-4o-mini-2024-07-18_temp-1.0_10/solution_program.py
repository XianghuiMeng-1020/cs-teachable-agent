def check_winner(log_file, player_name, lucky_number):
    player_name = player_name.lower().strip()
    lucky_number = str(lucky_number).strip()
    with open(log_file, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            name, number = line.rsplit(' ', 1)
            if name.lower().strip() == player_name and number == lucky_number:
                return True
    return False