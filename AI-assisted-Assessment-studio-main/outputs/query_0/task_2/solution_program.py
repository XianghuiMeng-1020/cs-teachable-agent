def play_game(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    results = []

    for line in lines:
        name, bet_number = line.strip().split(':')
        bet_number = int(bet_number)
        dice_roll = ((len(name) * bet_number) % 6) + 1
        if bet_number == dice_roll:
            results.append(f"{name}:win")
        else:
            results.append(f"{name}:lose")

    with open(file_path, 'w') as f:
        for result in results:
            f.write(result + '\n')