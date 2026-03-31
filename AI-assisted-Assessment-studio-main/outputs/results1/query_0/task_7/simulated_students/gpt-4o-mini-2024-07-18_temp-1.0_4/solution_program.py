def game_of_chance(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    score = 10
    bet_amount = 0

    for line in lines:
        line = line.strip()
        if line.isdigit():
            bet_amount = int(line)
            if bet_amount > score:
                bet_amount = 0
        elif line == 'win':
            score += bet_amount
        elif line == 'lose':
            score -= bet_amount
        elif line == 'draw':
            continue

    with open('result.txt', 'w') as result_file:
        result_file.write(str(score))