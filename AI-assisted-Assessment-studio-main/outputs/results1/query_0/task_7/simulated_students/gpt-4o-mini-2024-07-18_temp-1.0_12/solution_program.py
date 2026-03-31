def game_of_chance(filename):
    score = 10
    bet = 0
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.isdigit():
                bet = int(line)
            elif line == 'win':
                score += bet
            elif line == 'lose':
                if bet <= score:
                    score -= bet
            elif line == 'draw':
                continue
    with open('result.txt', 'w') as result_file:
        result_file.write(str(score))