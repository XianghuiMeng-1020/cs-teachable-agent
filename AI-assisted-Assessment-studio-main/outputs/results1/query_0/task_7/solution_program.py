def game_of_chance(filename):
    score = 10
    bet = 0
    with open(filename, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if line.isdigit():
            bet = int(line)
        elif line in ['win', 'lose', 'draw']:
            if line == 'win' and score >= bet:
                score += bet
            elif line == 'lose' and score >= bet:
                score -= bet
            elif line == 'draw':
                pass

    with open('result.txt', 'w') as result_file:
        result_file.write(str(score))
