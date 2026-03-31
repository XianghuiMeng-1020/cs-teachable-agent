def check_winner(log_file, player_name, lucky_number):
    player_name = player_name.strip().lower()
    lucky_number = str(lucky_number)
    with open(log_file, 'r') as file:
        for line in file:
            line = line.strip().split()
            if len(line) >= 2:
                name = line[0].lower()
                number = line[1]
                if name == player_name and number == lucky_number:
                    return True
    return False