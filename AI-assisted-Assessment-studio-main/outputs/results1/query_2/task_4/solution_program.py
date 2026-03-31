def check_winner(log_file, player_name, lucky_number):
    with open(log_file, 'r') as file:
        lines = file.readlines()
    player_name = player_name.lower()
    for line in lines:
        parts = line.strip().split()
        if len(parts) == 2 and parts[0].lower() == player_name and parts[1].isdigit():
            if int(parts[1]) == lucky_number:
                return True
    return False
