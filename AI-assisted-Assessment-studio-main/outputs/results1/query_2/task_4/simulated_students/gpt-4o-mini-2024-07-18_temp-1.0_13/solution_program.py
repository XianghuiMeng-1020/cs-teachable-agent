def check_winner(log_file, player_name, lucky_number):
    player_name = player_name.lower().strip()
    with open(log_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                name, number = line.rsplit(' ', 1)
                if name.lower() == player_name and int(number) == lucky_number:
                    return True
    return False