def check_winner(log_file, player_name, lucky_number):
    player_name = player_name.lower().strip()
    lucky_number = str(lucky_number)
    with open(log_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.strip():
                name, number = line.split()
                if name.lower() == player_name and number == lucky_number:
                    return True
    return False