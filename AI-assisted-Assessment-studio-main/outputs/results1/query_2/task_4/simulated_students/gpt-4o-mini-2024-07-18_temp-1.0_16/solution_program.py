def check_winner(log_file, player_name, lucky_number):
    player_name = player_name.lower().strip()
    lucky_number = str(lucky_number)
    with open(log_file, 'r') as file:
        for line in file:
            entry = line.strip().split()
            if len(entry) == 2:
                name, number = entry[0], entry[1]
                if name.lower() == player_name and number == lucky_number:
                    return True
    return False